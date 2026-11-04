# Version JPEG deployment packages

Status: Implemented
Implementation commit: Pending

## Problem and changes
The old installed logger rejects recording because its parser predates that
section. Rebuilt logger wheels still had version 0.1.0, allowing installs to retain
stale code. Assign distinct patch versions and minimum compatible dependencies:
bullet_msgs 0.1.1, mcap_bagger 0.1.2, msp_link 0.1.1, msp_telem_logger 0.1.1,
flight_lens 0.1.1.
Recorder/logger/viewer require bullet-msgs>=0.1.1; logger requires
mcap-bagger[jpeg]>=0.1.2 and GPS-capable msp-link>=0.1.1. Add logger --version using installed metadata.
Document explicit local-wheel upgrades and verify installed config/resources.
Do not rewrite user YAML, delete old wheels, commit or push.

## Verification
uv lock check; build five wheels; install updated logger and dependencies over
previous versions in a temporary venv without force-reinstall; verify --version,
JPEG config loading, dependency versions and real MCAP/Flight Lens integration.

## Outcome
Built distinct-version wheels in deploy/. Verified upgrading an isolated older
installation without force-reinstall, correct --version output, packaged JPEG
configuration loading and compatible dependency metadata. All 44 installed logger
tests passed; after binding the GPS-capable MSP library, both raw/JPEG real-recorder
Flight Lens readback cases passed again. uv.lock validates. Documented exact
Radxa wheel install commands and separate Flight Lens viewer upgrade. Remote
Radxa installation remains a user action; no remote access was available.
