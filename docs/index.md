# Workspace documentation

See [Project and workspace structure](project-structure.md) for the directory
layout, project responsibilities, Git ownership and where to put changes.

## Ownership

The workspace repository owns integration profiles in root `config/`, shared
launch tools, dependencies, terrain assets and cross-project documentation.
Each of the eleven directories under `projects/` is independently managed;
project-specific docs, configuration defaults and plans stay with that project.
The workspace root and all eleven projects are initialized as separate local
Git repositories published separately on GitHub. See the
[repository list and clone instructions](repositories.md). There are no Git
submodules. Recovering older history is a separate operation. Initial
snapshot hashes are recorded in the [commit plan](../plan/0003-initial-repository-commits.md).

## Paths and launch flow

`tools/run_all.sh` resolves the workspace root from its own location, builds the
renderer in `projects/bullet_render`, opens the viewers and invokes
`tools/run_flight.py` with absolute workspace profile paths. The flight launcher
starts the recorder before Godot, physics and the application, using the project
directories as worker working directories. It shuts the recorder down last.

Workspace recording settings live in `config/app.json`. New MCAPs and process
logs go under root `recordings/`; old recordings retain their historical source
paths. Producers record the actual newly loaded paths in future snapshots.
Project revision collection looks for each project's own Git metadata and never
substitutes an enclosing workspace commit for an uninitialized project.

The renderer and physics share `assets/terrain/terrain_heightmap.f32`. Godot's
terrain export script writes the heightmap, manifest and mesh into that same
directory. Native build files and shared environment paths must resolve through
the new project locations; cached build paths from before migration are stale.

## Migration and development

The uv workspace lists `projects/<name>` members and retains the shared root
lockfile. Synchronize with `uv sync --locked --all-packages --all-extras --all-groups`.
Dependencies were not upgraded for the directory move. VS Code's workspace file
uses the new paths while retaining project display names and task labels.

Use root `plan/` for cross-project work and project `plan/` directories for local
changes. Historical plans keep the paths that were valid when written. Current
commands and current architecture documentation use the new paths.

See the [workspace README](../README.md) for setup, launch and Git workflows, and
the [migration plan](../plan/0001-independent-project-layout.md) for verification.
