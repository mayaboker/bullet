# Bullet workspace

This repository owns the integration of twelve independently managed projects.
Each project lives under `projects/` and retains its own source, tests, defaults,
documentation and plans. The workspace does not use Git submodules.

Project repositories are being published publicly on GitHub. See the
[repository list and clone instructions](docs/repositories.md).

## Layout and ownership

- `projects/`: independent project checkouts, ignored by workspace Git.
- `config/`: shared flight profiles and workspace recording configuration.
- `docs/`: workspace setup and integration documentation.
- `tools/` and `tests/`: launchers, integration checks and orchestration tests.
- `plan/`: cross-project implementation plans and verification records.
- `experiments/`: research scripts, formerly `r_and_d/`.
- `assets/terrain/`: shared terrain mesh, heightmap and manifest.
- `recordings/`: generated MCAPs, indexes and launch-session logs; ignored.
- `deploy/`: generated Python wheels; ignored.
- `.venv/`, `pyproject.toml`, `uv.lock`: shared environment and dependency lock.

## Setup

Place the project checkouts in `projects/` using their existing repository URLs.
The workspace does not clone, initialize or configure repositories automatically.

```bash
uv sync --locked --all-packages --all-extras --all-groups
```

Open `bullet.code-workspace` in VS Code. Project names remain unchanged in the
editor; the root task **Bullet: Run all** selects the backend and drone model.

## Build a Python wheel

Open `bullet.code-workspace`, run **Tasks: Run Task → Bullet: Build Python wheel**,
and select a project from the list. The wheel is written to workspace-root
`deploy/`, which is ignored by Git. Wheels for other projects remain in that
directory. The native `bullet_render` project is excluded because it is not a
Python package.

Equivalent command from the workspace root, for example:

```bash
uv build --package bullet-app --wheel --out-dir deploy
```

To build every Python package at once, run **Tasks: Run Task → Bullet: Build all
Python wheels**. This includes `msp_telem_logger` and its sibling dependencies;
the non-package `bullet_render` project is skipped.

```bash
uv build --all-packages --wheel --out-dir deploy
```

Bullet View and FlightLens wheels include application icons. After installing a
GUI wheel in your chosen environment, run `bullet-view --install-launcher` or
`flight-lens --install-launcher` from that environment to add Linux menu and
desktop entries. Use `--menu-only` to skip the desktop shortcut, or
`--uninstall-launcher` to remove the managed entries. Building a wheel does not
register shortcuts automatically. See each GUI project's README for details.

The original flight-themed assets can be regenerated in the shared environment:

```bash
QT_QPA_PLATFORM=offscreen uv run --locked --all-packages python tools/generate_gui_icons.py
```

## Production launcher

See [production bringup](docs/production-bringup.md) for the installed headless
launcher and MAVLink/Godot recording authority. Preview a launch without side effects:

```bash
uv run --locked --package bullet-bringup bullet-bringup run --config projects/bullet_bringup/config/bringup.yaml --dry-run
```

## Run

From the workspace root, build and launch the full internal heavy-quad workflow:

```bash
bash tools/run_all.sh internal heavy_quad
```

Other combinations are `internal racer`, `betaflight racer`, and
`betaflight heavy_quad`. The Betaflight workflow requires its existing SITL setup.
The **Bullet: Run all** task uses [config/operator_controls.yaml](config/operator_controls.yaml):
manual arming and MAVLink recording. Start the Godot session to enable feedback,
then use Bullet View: **Apply height → Arm → wait for armed idle → Start mission**.
Arm alone keeps minimum throttle. **Start recording** and **Stop recording** are
independent buttons above the tabs; Stop waits for the MCAP to finalize.
Restart the launcher after changing operator controls. Set `arming_mode` to
`automatic` or `recording_control_source` to `godot` to restore either behavior.
Direct `tools/run_flight.py` calls without `--controls-config` retain their legacy
automatic/Godot defaults; pass `--controls-config config/operator_controls.yaml`
to use the workspace settings.

To launch flight services directly after building the renderer, first start
`bullet-visual --config projects/bullet_visual/config/zmq.yaml` in the shared
environment, then run:

```bash
uv run --locked --all-packages --all-extras --all-groups python tools/run_flight.py \
  --physics-config config/internal_heavy_quad.yaml \
  --controls-config config/operator_controls.yaml \
  --mission-config config/bullet_profile_heavy_quad.yaml
```

Configuration arguments resolve against the calling directory before workers
start. Workspace recordings default to `recordings/` through `config/app.json`;
`--mcap-output-dir` overrides this for one launch. Process logs are saved in
`recordings/launch_<timestamp>/`.

```bash
uv run --locked --package flight-lens flight-lens
uv run --locked --package bullet-view bullet-view
uv run --locked --all-packages python tools/cleanup_flight.py --dry-run
```

## Git and verification

The workspace root and all twelve projects have independent local Git
repositories. Remote configuration and pushing are
managed separately for each repository.
Manage workspace changes from this directory and project changes from their
individual directories. The workspace ignores `/projects/`; it does not record
project revisions as Git links. Environment and launch commands do not initialize
repositories automatically.

```bash
git status --short
git -C projects/bullet_app status --short
```

Reload `bullet.code-workspace` to refresh VS Code Source Control. Select the
appropriate repository before staging or committing. See the
[structure guide](docs/project-structure.md#git-ownership) for ownership details.

Run orchestration tests from the workspace root:

```bash
uv run --locked --all-packages pytest -q tests
```

Run each project's tests from its own directory to preserve its test/import
configuration. See [workspace details](docs/index.md) and
[migration record](plan/0001-independent-project-layout.md).

### Standalone camera and MSP recording

[`msp_telem_logger`](projects/msp_telem_logger/README.md) records USB/MIPI/ZMQ
camera images (JPEG by default) plus read-only Betaflight attitude, altitude, GPS and status. It
starts its own MCAP recorder. All MSP request intervals default to 0.1 s (10 Hz)
and are independently configured in YAML:

```bash
uv run --locked msp-telem-logger --print-example usb > logger.yaml
uv run --locked msp-telem-logger --config logger.yaml
```
