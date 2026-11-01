# Independent project workspace layout

## Goal and ownership
Move eleven projects under projects/ without submodules. Workspace owns root
config, docs, tools, integration tests, shared uv files, experiments and assets.
Move folders only: do not initialize Git, set remotes, commit or push.

## Implementation
1. Preserve complete project directories and existing contents while moving them.
2. Move r_and_d to experiments and terrain to assets/terrain.
3. Move workspace orchestration tools and their four test modules out of the
   renderer. Keep run_godot.sh and renderer-native tools with the project.
4. Update uv members/lock source paths, VS Code, launchers, checks, cleanup,
   provenance, terrain, shared environment/native builds and current docs.
5. Add workspace config/app.json for root recordings and use it in the launcher.
   Resolve caller paths before changing worker directories. Launch logs belong
   under recordings/. Keep historical plans and recording contents unchanged.
6. Document setup, independent Git ownership and new launch commands. No symlinks.

## Interfaces and defaults
Project paths become projects/<name>. Workspace commands live in tools/; root
config remains workspace-owned. Controller tuning, package names, dependency
versions and recorded wire schemas remain unchanged. No repository URLs or
revision manifest are added. Generated environments/caches may be refreshed.

## Verification
Inventory preservation; lock/sync and imports; load all workspace profiles and
preserve 0.08/0.08/0.05 rate gains and 5.5 m/s descent. Test workspace orchestration
and affected project suites, reconfigure/build native renderer, validate terrain,
and smoke-test internal heavy-quad launch plus FlightLens/Bullet View. Verify
root recordings/config provenance and workspace ignore boundaries.

## Status
Implemented; migration checks passed. Three unchanged pre-existing physics-suite
checks remain failing, described below. No repository was initialized or committed.

## Verification results
- Inventoried 635 source/asset files before moving: none missing afterward.
  Historical project plans and terrain files retain their original hashes.
  Complete project directories, including ignored dependency sources and existing
  build artifacts, were moved. Old generated CMake trees were retained with
  `-before-layout` names while active build trees were regenerated.
- uv lock/sync passed; all 50 package versions are unchanged. All ten importable
  Python packages resolve into projects/; the renderer is the eleventh workspace
  member. Root pytest discovery is limited to workspace tests; package suites
  continue using their own project configurations.
- All eight root YAML profiles load, shared terrain loads, both heavy-quad
  descent limits remain 5.5 m/s and internal rate gains remain [0.08, 0.08, 0.05].
  Both the workspace and application recording defaults resolve to root recordings/.
- Passed: workspace 8; bullet_app 168; bullet_msgs 173; los_tracking 127;
  flight_lens 92; bullet_view 25; mcap_bagger 87; msp_link 9;
  bullet_perception 12; bullet_visual 7; bullet_render 28 tests.
- Physics full-suite run: 708 passed, five failed. The terrain-path failure was
  fixed and passed; the analysis-publication timing check passed on rerun.
  Three unchanged checks still fail: two PlotJuggler tests expect tasks absent
  from the existing empty .vscode/tasks.json, and one sensor test expects no
  rangefinder despite the existing basic profile enabling it. Their source/task
  files match the pre-migration inventory; unrelated behavior was not changed.
- Native renderer configured and built from relocated existing pinned sources;
  repeated-build and native transport checks passed. Godot terrain export script
  passed --check-only; real scene smoke checks loaded the moved terrain.
- The isolated heavy-quad integration check reached LOS_APPROACH, checked 419
  exact source associations and 32 LOS diagnostic samples, and verified command
  expiry (0.059 s), process restart and reset. Its migrated harness now starts
  bullet_visual on a separate test endpoint; otherwise the existing harness
  receives no target observations. Report: /tmp/bullet-layout-flight-final/report.json.
- The actual root launcher reached READY with all four worker logs under
  recordings/launch_20261101T141618.495895Z/. Relative caller profile arguments
  resolved to root config/ and worker paths resolved to projects/.
- FlightLens and Bullet View opened and remained running from /tmp on the desktop.
  FlightLens default config lookup was made independent of the launch directory,
  and startup also accepts a missing optional config without a KeyError.
- Workspace ignore rules exclude /projects/, /.venv/ and /recordings/; root config,
  docs, tools and plans remain outside these exclusions. No submodules, project
  aliases, Git initialization, remote configuration, commits or pushes were added.

Logs and inventory: /tmp/layout-*-tests*.log, /tmp/bullet-layout-inventory.json,
/tmp/layout-root-launch-result.json. Test/smoke processes started here were stopped.

## Implementation commit
Pending
