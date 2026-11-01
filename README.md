# Bullet workspace

This repository owns the integration of eleven independently managed projects.
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
- `.venv/`, `pyproject.toml`, `uv.lock`: shared environment and dependency lock.

## Setup

Place the project checkouts in `projects/` using their existing repository URLs.
The workspace does not clone, initialize or configure repositories automatically.

```bash
uv sync --locked --all-packages --all-extras --all-groups
```

Open `bullet.code-workspace` in VS Code. Project names remain unchanged in the
editor; the root task **Bullet: Run all** selects the backend and drone model.

## Run

From the workspace root, build and launch the full internal heavy-quad workflow:

```bash
bash tools/run_all.sh internal heavy_quad
```

Other combinations are `internal racer`, `betaflight racer`, and
`betaflight heavy_quad`. The Betaflight workflow requires its existing SITL setup.
The launcher opens Godot; press Start to begin the mission.

To launch flight services directly after building the renderer, first start
`bullet-visual --config projects/bullet_visual/config/zmq.yaml` in the shared
environment, then run:

```bash
uv run --locked --all-packages --all-extras --all-groups python tools/run_flight.py \
  --physics-config config/internal_heavy_quad.yaml \
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

The workspace root and all eleven projects have independent local Git
repositories with local baseline commits. Remote configuration and pushing are
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
