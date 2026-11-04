# Five-second MSP rate log

Status: Implemented
Implementation commit: Pending

## Scope

- Log one multiline INFO summary every five seconds for attitude, altitude, GPS and status.
- Show each configured target rate and measured transport send and successful-response rates in Hz.
- Keep counts across MSP reconnects so a reporting interval includes disconnection time.
- Preserve existing one-second MSP delivery metrics and configuration defaults.
- Publish `msp-link` 0.1.2 and `msp-telem-logger` 0.1.3 with a matching minimum dependency.

## Verification

- Cumulative-count test covers successful responses, firmware rejection and reconnect.
- Logger test covers the five-second cadence, per-type rates and zero-activity interval.
- `uv run --locked --all-packages pytest projects/msp_link/tests projects/msp_telem_logger/tests -q`: 64 passed.
- After splitting the summary into lines, `uv run --locked --all-packages pytest projects/msp_telem_logger/tests/test_logger.py -q`: 45 passed.
- Locked CLI reports logger version 0.1.3; both wheels build, and logger wheel metadata requires `msp-link>=0.1.2`.

## Outcome

Implemented the periodic rate summary in `msp_telem_logger` using cumulative
transport-event totals from `msp_link`. No repository was committed or pushed.
