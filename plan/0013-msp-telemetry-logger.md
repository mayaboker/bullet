# MSP telemetry logger

Status: Implemented
Implementation commit: Pending

## Goal
Standalone uv application using msp_link and bullet_visual, recording raw frames,
attitude, altitude, GPS and status through ZMQ to an owned mcap_bagger process.

## Agreed interfaces and defaults
- Betaflight serial /dev/ttyACM0, 115200 baud; USB device 0; immediate recording.
- YAML requests.attitude/altitude/gps/status each interval_s=0.1 by default.
- Extend bullet_msgs analysis_msp.json compatibly with hardware source and GPS.
- Add typed MSP_RAW_GPS decoding in msp_link; no control writes or derived velocity.
- Independent camera and MSP workers, bounded queues, monotonic scheduling,
  skip missed periods, expose stale/unsupported data and drop counters.
- Recorder readiness/recording acknowledgement, heartbeat and finalization;
  opt-in recorder --exit-after-recording for normal child exit,
  dedicated configurable loopback ports 5585–5588, one MCAP per application run.
- Workspace/lockfile/wheel picker integration, packaged examples and documentation.

## Verification
GPS decoding and failure cases; polling/configuration; legacy and hardware schema;
fake MSP plus synthetic frames and real recorder MCAP readback; failure cleanup;
wheel CLI/resources from outside repository. Physical hardware not available.

## Scope
No detection/bbox, arming, RC writes, runtime config reload, Git init/commit/push.

## Outcome
Implemented with packaged USB/MIPI/ZMQ profiles, hardware-compatible shared MSP
schema, typed GPS decoder, independently configurable 10 Hz default polling and
owned recorder finalization. Existing service defaults are preserved.

Verification: 226 logger/MSP/shared-schema tests, 95 recorder tests (1 skipped),
7 visual tests and 15 workspace tests passed (343 passed, 1 skipped total).
Built the application and sibling wheels and installed them into an isolated
Python environment. All 22 logger tests passed from /tmp using installed packages,
including real recorder subprocess MCAP pixel/telemetry readback. Help and all
packaged configuration examples work outside the repository. No physical hardware
was exercised. No repository initialized, committed or pushed.
