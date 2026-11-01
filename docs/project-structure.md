# Project and workspace structure

The workspace brings eleven projects together into one development environment.
The workspace owns integration settings and tools. Each project owns its source,
tests and documentation and is managed independently in Git, without submodules.
The workspace root and all eleven project folders have their own local Git
repository with a local baseline commit. These snapshots start new local history;
they do not recover historical commits. No remotes have been configured here.

## Directory layout

```text
bullet/
├── .git/                        # Workspace repository metadata
├── AGENTS.md                    # Workspace development instructions
├── README.md                    # Setup and launch commands
├── bullet.code-workspace        # VS Code folders and tasks
├── pyproject.toml               # uv workspace members and root test settings
├── uv.lock                      # Shared dependency versions
├── .python-version              # Shared Python version
├── .gitignore                   # Workspace Git exclusions
├── .vscode/                     # Workspace editor settings
├── config/                      # Integration profiles and recording settings
├── docs/                        # Workspace documentation, including this guide
├── plan/                        # Cross-project plans and verification records
├── tools/                       # Launchers, cleanup and integration checks
├── tests/                       # Tests for workspace orchestration
├── experiments/                 # Research scripts and prototypes
├── assets/
│   └── terrain/                 # Shared mesh, heightmap and manifest
├── projects/
│   ├── bullet_app/
│   ├── bullet_drone/
│   ├── bullet_msgs/
│   ├── bullet_perception/
│   ├── bullet_render/
│   ├── bullet_view/
│   ├── bullet_visual/
│   ├── flight_lens/
│   ├── los_tracking/
│   ├── mcap_bagger/
│   └── msp_link/
├── recordings/                  # Generated MCAPs, indexes and process logs
└── .venv/                       # Shared Python environment
```

## What each project does

| Project | Responsibility |
|---|---|
| [bullet_app](../projects/bullet_app/) | Runs the mission, consumes visual detections and sensor feedback, applies LOS guidance, and publishes flight commands and telemetry. |
| [bullet_drone](../projects/bullet_drone/) | Simulates drone dynamics, sensors and flight-controller behavior using PyBullet. |
| [bullet_msgs](../projects/bullet_msgs/) | Defines shared message contracts, schemas and shared-memory image transport. |
| [bullet_perception](../projects/bullet_perception/) | Provides reusable image-processing and target-detection utilities. |
| [bullet_render](../projects/bullet_render/) | Renders the landscape and camera in Godot and provides the native ZeroMQ camera adapter. |
| [bullet_view](../projects/bullet_view/) | Displays live MAVLink telemetry, logs and application parameters, including parameter editing. |
| [bullet_visual](../projects/bullet_visual/) | Captures images, runs perception and publishes target bounding boxes. |
| [flight_lens](../projects/flight_lens/) | Opens MCAP recordings for offline flight analysis, issue investigation and configuration inspection. |
| [los_tracking](../projects/los_tracking/) | Converts timestamped bounding boxes, attitude and altitude into bounded guidance demands. |
| [mcap_bagger](../projects/mcap_bagger/) | Records images and telemetry into MCAP files. |
| [msp_link](../projects/msp_link/) | Provides MSP communication over TCP or serial for flight-controller integration. |

## Where changes belong

| Change | Location |
|---|---|
| Settings for a complete flight configuration, such as the heavy-quad mission and physics profiles | Root `config/` |
| Workspace recording destination | Root `config/app.json` |
| Launching or checking several applications together | Root `tools/` and `tests/` |
| Shared setup, architecture or project-ownership documentation | Root `docs/` |
| A plan affecting multiple projects | Root `plan/` |
| Library or application implementation | The relevant project's `src/` |
| Project-specific defaults, standalone examples and tests | The relevant project's configuration, example and test folders |
| Project-specific design documentation and plans | The relevant project's `docs/` and `plan/`, where present |

Project layouts vary. Python packages normally use `src/<package>/` and `tests/`.
The renderer also has `src/native/`, `godot/` and native build configuration.
Each project's `README.md` and any `AGENTS.md` describe its own conventions.

## Git ownership

The workspace repository tracks root configuration, documentation, tools, tests,
assets and shared dependency files. Its `.gitignore` excludes `/projects/`, so
project contents are managed by their own repositories. It also excludes
`/recordings/` and `/.venv/` because these are generated locally.

Commit workspace changes from the workspace root and project changes from the
corresponding project directory. A workspace commit does not commit project
changes or pin their revisions. Each project has its own `.git/` metadata; there
is no workspace `.gitmodules` file. Launch and environment setup commands do not
initialize repositories automatically.

Check workspace and project changes separately:

```bash
git status --short
git -C projects/bullet_app status --short
```

Reload `bullet.code-workspace` in VS Code to discover all twelve repositories.
Select the repository in Source Control before staging or committing its files.

## Shared environment and launch flow

The root `pyproject.toml` lists all `projects/<name>` workspace members. They use
one root `.venv/` and `uv.lock`, while retaining their own package manifests.
Synchronize from the workspace root:

```bash
uv sync --locked --all-packages --all-extras --all-groups
```

Open [bullet.code-workspace](../bullet.code-workspace) for the editor's project
folders and tasks. To build and launch the internal heavy-quad workflow:

```bash
bash tools/run_all.sh internal heavy_quad
```

The workspace launcher selects root profiles, builds the renderer, starts the
viewers and perception service, and launches the recorder and flight services.
Workers run in their own project directories. Configuration paths are resolved
before those workers start.

MCAP files go into root `recordings/` by default. Each launch writes separate
worker logs into `recordings/launch_<timestamp>/`. Shared terrain is read from
`assets/terrain/` by the renderer and configured physics profiles.

Run workspace tests from the root with `uv run --locked --all-packages pytest -q`.
Run each project's tests from that project's directory so its own test settings
apply. See the [workspace README](../README.md) for additional launch commands
and the [documentation index](index.md) for integration details.
