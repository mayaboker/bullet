# Production bringup

[bullet_bringup](../projects/bullet_bringup/README.md) is the installed headless
launcher for the application processes. It launches mcap_bagger, bullet_visual
and bullet_app, without Godot, physics, SITL or desktop viewers.

## Select recording authority

The launch YAML chooses exactly one controller:

```yaml
# Recorder service configuration.
recorder:
  # Existing recorder configuration, relative to the launch YAML.
  config: recorder.yaml
  # mavlink (production default) or godot; restart to change authority.
  control_source: mavlink
```

In MAVLink mode, the application relays command 31011 (`MAV_CMD_USER_2`) to the
recorder over dedicated recording/state and recording/status ZMQ channels.
`param1=1` starts MCAP recording; `param1=0` finalizes it; other parameters are
zero. Commands use the existing application MAVLink connection (default UDP
14551, target system/component 1/1). Success is acknowledged only after recorder
confirmation. Each Start-to-Stop interval is a separate file. Processes start idle.

In Godot mode, the existing physics simulation/state lifecycle controls recording.
MAVLink recording commands are denied. Godot/physics are external to the production
launcher; do not run two launchers that duplicate application processes/ports.

The same ZMQ lifecycle pattern is used in both modes, but MAVLink recording state
never changes flight or simulation state. Recording state is repeated at 1 Hz;
three seconds without updates closes the current recording. Source changes are
configuration changes applied by restarting, not simultaneous competing controls.

## Development and deployment

From the workspace root:

```bash
uv run --locked --package bullet-bringup bullet-bringup run \
  --config projects/bullet_bringup/config/bringup.yaml --dry-run
```

The example camera uses USB index 0. Edit the deployment camera configuration
before launching without --dry-run. Mission configuration defaults to null
(detection-only). Adding a mission profile uses existing application behavior;
hardware flight-feedback integration remains separate.

All configuration references resolve relative to the launch YAML. Process logs
are stored under its log_dir; the recorder configuration owns the MCAP output
directory. The default records existing JSON streams, not raw USB/MIPI images.
User shutdown or any child exit stops app/visual first and recorder last.

The project's wheel-bundle helper builds the launcher and runtime dependencies
for a matching Linux/Python target. Installation uses one virtual environment
and requires neither uv nor source checkouts at runtime. See the project README
for offline installation, command examples and platform prerequisites.

V1 has no automatic restarts, systemd startup, health-monitor UI or configuration
editor. The existing simulation launchers remain unchanged.

## Manual flight controls

Production `app.arming_mode: manual` requires separate Arm and Start mission
commands in Bullet View. The example remains detection-only until a compatible
mission profile and fresh flight feedback are supplied. See
[manual flight controls](../projects/bullet_msgs/docs/manual-flight-control.md)
for command/state semantics, confirmed height handling and the disarm latch.

Bullet View also provides persistent **Start recording** and **Stop recording**
buttons. These work with `recorder.control_source: mavlink` independently of flight;
Stop confirms only after MCAP finalization. With Godot authority the viewer shows
that authority and disables its recording buttons.

The workspace **Bullet: Run all** task has its own source-controlled settings in
[operator_controls.yaml](../config/operator_controls.yaml), selecting manual
Arm/Start and MAVLink recording. Restart that task after changing these settings.
