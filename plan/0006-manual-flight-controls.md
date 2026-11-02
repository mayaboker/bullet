# Manual flight controls and takeoff-height slider

- Status: Implemented; verification passed on 2026-11-02.
- Implementation commit: `41ce23a7fbbc08f5e63f7b65faf6bb1a6ada9f72`
- Destination: Main conversation. Read applicable project instructions and current changes before implementation.

## Scope

Add a persistent flight-control panel to `bullet_view`, with commands routed through `bullet_app` over MAVLink. Support the existing simulator and Betaflight/MSP backend through the application's control path. A detection-only session without valid flight feedback cannot arm.

Expected affected projects: `bullet_view`, `bullet_app`, shared MAVLink/message definitions in `bullet_msgs`, and production configuration/examples in the bringup project where required. Confirm current repository paths before editing. Coordinate with ongoing recording-control and bringup changes; preserve unrelated work. Do not commit or push without a separate request.

## User interface

Provide:

- Arm button.
- Horizontal takeoff-height slider, synchronized numeric editor and Apply button.
- Start mission button, separate from Arm.
- Disarm button, with a confirmed emergency-disarm action when flying.
- Actual remote arming state and remotely confirmed takeoff height.

Use metres above the launch datum. Allow 0.1–100.0 m in 0.1 m steps, matching the existing shared takeoff-height limits; verify those definitions before implementation.

Keep draft and applied height separate. Apply sends the value and waits for acknowledgement plus matching remote readback. Show the applied value as unknown until confirmed; a local 20 m fallback must not appear remotely confirmed. Start mission is disabled while Apply is pending or the draft differs from the applied value.

Height may change before flight and while armed idle. Lock it once the mission starts. Arm must leave the vehicle at idle, without starting takeoff. Start mission requires confirmed armed-idle state and a confirmed height.

Worker code owns network communication; presenter code coordinates state; view code owns widgets. Match acknowledgements to the intended command and target. Display acknowledgement and observed vehicle state separately.

Disable Arm, Apply and Start when feedback is stale, the backend is unavailable, or a conflicting command is pending. Keep Disarm available for a known target while Arm or Start is pending; cancel outstanding actions and retries when disarming. Emergency confirmation defaults to Cancel.

## Takeoff-height semantics

The selected height is above the captured launch datum, not a global altitude or target ground elevation. Do not reuse navigator `target_altitude_m`.

- An operator-applied height overrides scenario feedback for subsequent takeoffs during the current application run.
- The override survives episode reset and profile reload, and clears on application restart.
- Without an override, preserve the scenario-provided height and existing default behavior (currently 20 m).
- Capture the effective height when the mission starts and hold it fixed for that flight.
- Once the launch datum is captured, altitude goal equals launch datum plus captured takeoff height.
- Include effective height and its source in diagnostics and logs.

Verify existing initialization and feedback precedence before implementing this behavior.

## MAVLink command contract

Use the existing application MAVLink endpoint, not a new direct autopilot connection. Confirm command allocation against concurrent changes before adding constants.

| Action | Command | Parameters |
|---|---|---|
| Arm | `MAV_CMD_COMPONENT_ARM_DISARM` (400) | param1=1; remaining parameters=0 |
| Normal disarm | `MAV_CMD_COMPONENT_ARM_DISARM` (400) | param1=0; remaining parameters=0 |
| Emergency disarm | `MAV_CMD_COMPONENT_ARM_DISARM` (400) | param1=0, param2=21196; remaining parameters=0 |
| Start mission | `MAV_CMD_MISSION_START` (300) | All parameters=0 |
| Apply takeoff height | `MAV_CMD_USER_3` (31012), if still available | param1=height in metres; remaining parameters=0 |

Existing allocations observed during planning: USER1/31010 for reload; USER2/31011 for recording. Preserve their behavior. Reject force-arm requests, invalid values, unsupported parameters and commands without a valid flight session. Support normal disarm while idle; reject normal airborne disarm and require the explicitly confirmed emergency path.

Handle commands asynchronously so the MAVLink loop continues serving recording, reload and parameter traffic. For arm/disarm, acknowledge success only after fresh backend feedback confirms the requested state. Use a 5-second timeout and report failures clearly. Stale feedback means unknown state. Verify fresh MSP status is used for Betaflight, rather than a fallback that reports false disarmed state.

Expose remote state/readback using the existing telemetry convention, with planned names `ARM_MODE`, `ARM_VALID`, `MIS_READY` and `TAKEOFF_H`. Define their exact types, meanings and freshness handling in the shared protocol documentation. `TAKEOFF_H` must reflect the effective remote value; do not report a draft as applied.

## Mission and arming behavior

Add configurable `arming_mode` with `automatic` and `manual` values. Keep automatic as the default for existing simulation profiles; use manual in the production example.

- Manual Arm produces neutral controls/minimum throttle and enters armed idle.
- Start mission begins takeoff only after valid armed-idle confirmation.
- An explicit manual Arm or Disarm takes operator control for the rest of that application run; automatic progression resumes only after restart.
- Disarm must latch so the next tick, profile reload or episode update cannot rearm the vehicle.
- Emergency disarm immediately stops/aborts mission control and requests force disarm through the backend.
- After emergency disarm, require stopped/reset state and normal prearm readiness before another Arm.

Preserve existing automatic simulation startup where the operator has not taken manual control. Ensure the latch and mission state are updated in the owner thread, with thread-safe command dispatch.

## Implementation sequence

1. Inspect applicable project instructions, current uncommitted work, command allocation, mission state ownership and backend feedback paths.
2. Define shared command/state contracts and document takeoff-height precedence.
3. Implement application-side command dispatch, state transitions, override handling, feedback confirmation and disarm latch.
4. Add worker/presenter support and the persistent flight-control panel with slider, editor, Apply and status feedback.
5. Update production configuration and user documentation, preserving standalone defaults.
6. Run focused verification with uv and the shared lockfile, record results here, and leave implementation commit Pending until committed.

## Verification

Use fake or internal simulation backends; do not actuate physical motors during verification.

- Validate slider/editor synchronization, limits, non-finite inputs, Apply acknowledgement/readback, timeout, and unknown/stale state.
- Confirm Arm alone never starts takeoff, and Start requires armed-idle state and applied height.
- Confirm a nonzero launch datum produces datum + selected height as the goal.
- Check override precedence across feedback, reset, profile reload and application restart; lock the captured height during flight.
- Confirm normal disarm is denied airborne, emergency Cancel sends nothing, and confirmed emergency disarm aborts control and latches against rearming.
- Exercise pending Arm/Start cancellation, delayed acknowledgements, wrong-target messages, missing backend feedback and feedback timeout.
- Verify existing automatic profiles, recording commands, reload commands and parameter management still work.
- Validate changed launch/configuration paths and affected project behavior using uv and the workspace shared lockfile.

## Limits and follow-up

This plan does not add direct autopilot connectivity or airborne altitude adjustment. If a backend lacks trustworthy arming feedback, report that limitation and keep its controls unavailable until feedback support is implemented; never infer successful arming solely from sending a command.

## Handoff instruction

In the main conversation, request: "Implement plan/0006-manual-flight-controls.md. Preserve the ongoing changes and coordinate with the current bringup and MAVLink recording work."

## Implementation result — 2026-11-02

Implemented in bullet_app, bullet_view, bullet_msgs and bullet_bringup. Existing
recording/bringup work was preserved. No commits or pushes were made.

- Persistent MVP flight panel: Arm, synchronized height slider/editor, Apply,
  Start and confirmed emergency Disarm. Draft/applied values and ACK/observed
  state remain separate. Telemetry scrolls on smaller windows; gauges remain
  readable and the flight panel stays above both tabs.
- Shared strict MAVLink command contract and coherent 20 Hz remote state.
  ACK result_param2 identifies the action so delayed Arm ACKs cannot complete
  Disarm. Exact target/source/destination checks and no automatic flight retries.
- Owner-thread mailbox with Disarm preemption (Emergency has highest priority),
  5-second backend confirmation deadline and fresh actual MSP arming state.
  Emergency forces safe RC and schedules MSP command 99; stopped and observed
  disarmed state releases its block, with normal prearm checks before rearm.
- Application-run operator latch and height override survive episode reset,
  profile reload and parameter-driven mission replacement. Height/source/datum/
  goal are diagnosed and logged; height locks at mission start.
- CLI --arming-mode automatic|manual, automatic default; production bringup
  forwards app.arming_mode and its shipped example selects manual. Detection-only
  configuration remains unable to arm.
- Protocol/user docs are in each affected README and
  projects/bullet_msgs/docs/manual-flight-control.md.

### Verification outcome

529 tests passed using uv and the shared lockfile, from the respective project
folders with `uv run --locked --all-packages pytest tests -q`:

| Suite | Passed |
|---|---:|
| bullet_app | 195 |
| bullet_view (QT_QPA_PLATFORM=offscreen) | 31 |
| bullet_msgs | 182 |
| bullet_bringup | 21 |
| mcap_bagger | 92 |
| workspace | 8 |

Coverage includes automatic PyBullet startup, manual idle/Start, nonzero datum,
height precedence/reset/replacement, strict/non-finite inputs, stale/unknown MSP
status, pending action cancellation, emergency priority/Cancel/rearm, ACK routing,
timeouts, recording, reload and parameter management. A real MAVLink 2 UDP
Height→Arm→Start→Emergency roundtrip passed using a fake internal flight backend.
Qt widget rendering was visually inspected; resize/scroll and gauge sizing were
checked. All four changed projects built wheels. A fresh offline environment at
/tmp/bullet-manual-installed imported the installed app/messages/bringup wheels
and passed standalone CLI/configuration/protocol checks and bringup dry-run from
/tmp, without PYTHONPATH or DISPLAY. No physical motors or camera were actuated.

Physical Betaflight/MSP actuation remains unverified; MSP command 99 behavior was
checked against the pinned 2026.6.2 source, and its scheduler behavior tested with
a fake client. A camera-only production run still needs a compatible mission
profile and fresh flight-feedback provider before flight controls become ready.
Implementation commit: `41ce23a7fbbc08f5e63f7b65faf6bb1a6ada9f72`.

## Commit record — 2026-11-02

The verification notes above describe the pre-commit work. Implementation is
now committed; nothing was pushed. These are implementation hashes, rather than
the subsequent documentation commits that record them.

| Repository | Implementation commit |
|---|---|
| bullet_app | `41ce23a7fbbc08f5e63f7b65faf6bb1a6ada9f72` |
| bullet_view | `8653377251f426e1f1c6539191e2cd91480e447e` |
| bullet_msgs | `30c387e6f94917b2ff661375d28a365b5088cace` |
| bullet_bringup | `bb7371e66e2bbee1210142d8ea64b25e03ab1ba6` |
| workspace | `7a724df66b5e09d4b3be25a8ace6c20d73681aab` |
