# JPEG MCAP recording and bounded image overload

Status: Implemented
Implementation commit: Pending

## Goal and defaults
Compress images only at recorder output; native camera/live-stream FPS unchanged.
MSP logger defaults: recording.image_format=jpeg, jpeg_quality=75,
image_overflow_policy=drop_oldest. Generic recorder remains raw/strict by default.
Use optional Pillow/libjpeg-turbo JPEG backend (no hardware encoder promise).
Keep 64 MiB queue bound, evict only images, preserve telemetry, report drops.
Flight Lens reads RawImage and CompressedImage on demand and warns on loss.
Preserve primary recorder errors while cleaning up subprocesses and resources.

## Interfaces and work
- Recorder YAML: per-image image_format/raw|jpeg, jpeg_quality/1..95; top-level
  image_overflow_policy/error|drop_oldest. Image input layout and metadata unchanged.
- Shared recording_health gains optional nonnegative dropped_images counter.
- MSP logger forwards recording settings and selects mcap-bagger[jpeg].
- Flight Lens validates JPEG format/dimensions before decode, preserves old files.
- Package examples/docs, installed wheels, and raw/JPEG benchmark command.

## Verification
Configuration/backend failures, padded RGB/BGR JPEG pixels/timestamps/protobuf;
slow writer + bounded queue + telemetry + accurate image/metadata sequences;
strict overflow/disk failures; primary vs cleanup error; recording -> Flight Lens
first/middle/last previews and loss notice; installed wheel integration.
Benchmark CPU, file throughput, input/written FPS, drops and queue peak. Radxa
measurements require running on the device; no system packages installed here.

## Outcome and verification
Implemented JPEG MCAP output, native-FPS attempts with image-only eviction,
optional dropped_images health metadata, raw/JPEG Flight Lens decoding with size
checks, and primary-error-preserving recorder cleanup. Generic raw/strict defaults
remain. Added packaged JPEG profiles and a recorder-only raw/JPEG benchmark.

450 checks passed in separate successful processes: 107 recorder, 44 MSP logger,
186 shared-message and 113 Flight Lens checks (77 non-GUI, 16 app, 5 recording-tab,
15 desktop). The combined Flight Lens process passes assertions but aborts during
Qt shutdown with malloc_consolidate; each isolated group exits successfully. That
combined-test teardown issue is not hidden or reported as a clean full-suite run.

Installed updated wheels in an isolated Python environment: all 44 logger tests,
including real MCAP subprocess -> raw/JPEG Flight Lens playback, and all 11 new
recorder JPEG/overload tests passed. Both packaged config locations select JPEG.
Rebuilt bullet_msgs, mcap_bagger, msp_telem_logger and flight_lens wheels in deploy/.
uv.lock checked current. No commit/push performed.

Short desktop benchmark smoke (deterministic noise, 320x240, 30 FPS, 0.5 s): raw
3,473,916 bytes vs JPEG 718,781 bytes, no image drops, telemetry retained. JPEG CPU
was higher (about 10.8% vs 5.9% of one core). This is a mechanics check, not a
Radxa performance claim. Physical Radxa/storage/hardware encoder not exercised.
