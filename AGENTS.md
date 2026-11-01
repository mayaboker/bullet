# Workspace guidance

- The workspace owns root configuration, documentation, shared uv files, tools,
  integration tests, experiments and terrain assets.
- Projects under `projects/` are independent repositories, ignored by workspace
  Git. Do not add submodules or initialize repositories without authorization.
- Preserve each project's instructions, standalone defaults and public interfaces.
- Resolve workspace paths explicitly; do not depend on the caller's directory.
- Keep environments, builds, caches, process logs and recordings untracked.
- Save cross-project implementation plans under `plan/`, including scope,
  verification, status and implementation commit (`Pending` until committed).
- Use uv and the shared lockfile. Validate changed launch paths and affected
  project behavior. Do not commit or push unless requested.
