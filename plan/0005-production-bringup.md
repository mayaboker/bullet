# Production bringup and selectable recording authority

## Goal
Install bullet-bringup for a Linux companion, launching mcap_bagger, bullet_visual
and bullet_app with one YAML. Select MAVLink or existing Godot/physics recording
authority; launch idle and record only when the selected authority requests it.

## Implementation
- Create independent Python project projects/bullet_bringup with Click CLI,
  validated relative-path configuration, pure launch planning/dry-run, owned
  process lifecycle and logs. Add uv/VS Code integration and a wheel bundle helper.
- Add shared recording/state and recording/status contracts, controller/session/
  request identity, sequence and freshness validation. Ports default 5561/5562.
- Add recorder recording-control mode without changing default simulation mode.
  Repeat desired state at 1 Hz; close on 3 s silence; finalize before confirming.
- Relay MAV_CMD_USER_2 (31011), param1 1=start/0=stop, through bullet_app in both
  detector and mission modes. ACK after confirmation, fail after 5 s, preserve
  existing reload/parameter commands. Godot authority denies MAVLink recording.
- Recorder readiness precedes visual/application startup. Any child exit or user
  signal ends the stack, app/visual first and recorder last, bounded timeouts.
- Ship commented configurations and install/use docs; record existing message
  streams only. Save per-project plan records before implementation.

## Scope and defaults
No simulator/viewer launch, auto-restart, systemd, live configuration UI, raw USB
image publishing, hardware flight-feedback changes, commits or pushes. Existing
simulation behavior remains available. New project is an independent local Git
repository on main. Runtime must work without a source checkout or uv.

## Verification
Configuration/dry-run tests; real TCP/UDP MAVLink recording/ACK/readback tests;
idempotency, stale/silence/error cases and control-source isolation; process/signal
cleanup tests; existing app/recorder/shared-message suites; wheel build and fresh
environment install outside workspace. No real camera or flight actuation needed.

## Status
Implemented; verification passed.

## Implementation commit
`bb7371e66e2bbee1210142d8ea64b25e03ab1ba6`

## Verification results
- 20 bringup tests passed: configuration/dry-run, process startup/failure/signals,
  readiness timeout, partial startup and log-thread failure cleanup, real local
  MAVLink/ZMQ/MCAP roundtrip, Godot isolation and pending-command shutdown ACK.
- 173 application tests, 92 recorder tests, 182 shared-message tests and 8
  workspace tests passed (475 total). Existing simulation recording, reload and
  parameter handling remain covered by their regression suites.
- Tested new recording error paths: bad/stale/reordered messages, confirmation
  timeout, disk-open failure, writer failure, silence timeout, duplicate commands,
  closed-session protection and a fresh Start after recorder closure.
- Built /tmp/bullet-bringup-bundle-final with eight local runtime wheels plus
  locked third-party wheels (113 MB, Linux x86_64 / Python 3.12 build host).
  Installed offline into /tmp/bullet-bringup-installed and ran from /tmp with
  PYTHONPATH and display variables unset. Installed MAVLink start/stop/readback
  and pending-command shutdown passed. All eight local packages resolve from
  that venv; no simulator, Qt viewer or pytest packages are installed there.
- MAVLink/Godot dry-runs validated without creating logs or recordings. Existing
  dependency versions are preserved; uv lock --check and changed-file whitespace
  checks passed. No real camera capture or flight actuation was performed.
- Applied exception-risk-review to thread/socket/process cleanup. Fixed partial
  log-thread startup cleanup, worker-error finalization reporting, pending ACKs
  on app shutdown and restarting a previously closed recording session.
- New bringup repository is initialized on main; no commits, remotes, pushes or
  systemd services were added. Process logs/build wheels are outside source or
  ignored. Test-owned child processes were terminated.

Verification logs: /tmp/bringup-*-final.log; installed check:
/tmp/bringup-installed-final.log. Local sources and wheel payloads were compared.

## Commit record — 2026-11-02

The verification notes above describe the pre-commit work. Implementation is
now committed; nothing was pushed. These are implementation hashes, rather than
the subsequent documentation commits that record them.

| Repository | Implementation commit |
|---|---|
| bullet_bringup | `bb7371e66e2bbee1210142d8ea64b25e03ab1ba6` |
| bullet_app | `41ce23a7fbbc08f5e63f7b65faf6bb1a6ada9f72` |
| bullet_msgs | `30c387e6f94917b2ff661375d28a365b5088cace` |
| mcap_bagger | `e527a9aab189bde69e580b53b4bd5148cf7a7f85` |
| workspace | `7a724df66b5e09d4b3be25a8ace6c20d73681aab` |
