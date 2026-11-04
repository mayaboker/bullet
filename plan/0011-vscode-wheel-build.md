# VS Code project wheel build task

- Status: Implemented; verified 2026-11-02
- Implementation commit: Pending

Add Bullet: Build Python wheel to bullet.code-workspace. First show a pickString
list of the eleven buildable Python projects, using folder labels and distribution
names as values. Exclude the native, package=false bullet_render member. Run
uv build --package <selection> --wheel --out-dir <workspace-root>/deploy from the
explicit workspace root. Default to bullet_app; keep other deploy artifacts.
Ignore root deploy output in Git and document task usage. No dependency changes,
project packaging changes, publishing, installing or commits are requested.

Validate task JSON and picker values against workspace project manifests, build
the default selection through resolved task arguments, inspect the resulting
wheel, check deploy is ignored and check whitespace/shared lock consistency.

## Verification result

Task/input JSON parsed successfully; the picker exactly matches all eleven
buildable workspace manifests, excluding package=false bullet_render. Resolved
the default picker/task variables and executed the real task command, creating
deploy/bullet_app-0.1.0-py3-none-any.whl. ZIP CRC validation, module contents and
wheel metadata checks passed. git check-ignore confirms the output is excluded.
uv lock --check and git diff --check passed. No dependencies or project packaging
were changed, and nothing was installed, published or committed.
