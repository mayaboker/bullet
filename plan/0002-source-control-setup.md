# Source control for workspace and projects

## Goal
Initialize the workspace root and eleven projects/ directories as independent
local Git repositories, without submodules.

## Implementation
- Initialize missing repositories on main, preserving any existing repositories.
- Keep /projects/ ignored by workspace Git and complete project ignore rules for
  Python environments/caches, build outputs and generated recordings. Add the
  missing bullet_visual ignore file without removing existing exclusions.
- Enable VS Code Git auto-detection, retaining the explicit workspace/project
  folders. Update documentation with repository ownership and separate workflows.

## Interfaces and defaults
Twelve local repositories. Leave files unstaged. No identity changes, remotes,
commits, pushes or submodules. New metadata does not recover historical commits.
Existing project metadata, if encountered, is preserved.

## Verification
Verify each repository's own top-level path and branch, ignore boundaries,
visible source files, empty staging areas and absence of newly added remotes or
commits. Validate workspace JSON and existing project folder entries. VS Code
will discover repositories when the workspace is reloaded.

## Status
Implemented; verification passed. All twelve repositories were newly initialized
on main. Files remain unstaged. No commits, remotes or submodules were added.

## Verification results
- Each git rev-parse --show-toplevel resolves to its own exact directory, rather
  than inheriting the workspace repository. All twelve branches are main.
- Git status succeeds in every repository, with only untracked files. Every
  index is empty, every remote list is empty and no HEAD commit exists.
- git check-ignore confirms generated environment/cache/build/recording paths
  are excluded and README/source files are visible in each repository.
- Workspace project contents are ignored; root config, docs, tools, tests, plan,
  experiments and assets remain visible. Root .gitmodules is absent.
- Workspace JSON parses, Git auto-detection is enabled and all twelve repository
  paths are explicit workspace folders. Reload VS Code to refresh its UI.
- Added bullet_visual/.gitignore and completed other project ignore rules
  additively. No application behavior or source code was changed.
- Updated workspace README, documentation index and project-structure guide.
  Machine-readable verification: /tmp/bullet-source-control-verification.json.

No runtime tests were needed for repository metadata, ignore rules and editor
settings; verification used actual Git commands for all twelve repositories.

## Implementation commit
`8c47f8feecf28acc718d3dff57e24a779318b124`

## Repository snapshot record
Recorded snapshot: `8c47f8feecf28acc718d3dff57e24a779318b124` (workspace repository). This is the new local
baseline containing the current implementation, not a recovered historical commit.
