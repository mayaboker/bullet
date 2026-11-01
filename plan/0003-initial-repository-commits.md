# Initial commits for workspace and projects

## Goal
Commit the current workspace and all eleven independent projects as local
repository baselines, preserving their separate Git boundaries.

## Implementation
- Review untracked files, existing identity and ignore boundaries in all twelve
  repositories. Stage current nonignored files and create one initial snapshot
  commit per repository.
- Record actual snapshot hashes for completed plans that still have Pending
  commit metadata, without replacing historical hashes or marking pending work
  complete. Make plan-metadata updates as separate documentation commits.
- Record repository snapshot hashes here and verify all working trees are clean.

## Defaults and interfaces
Use the existing configured Git identity and main branches. Preserve ignored
environments, generated builds and recordings. No remote configuration or push.
These commits establish new local history; they do not restore old histories.
Any Pending completed-plan hash filled here identifies the current snapshot,
not an inferred historical implementation commit.

## Verification
Git status, staged-file ownership, cached diff checks, actual commit hashes and
clean working trees. Runtime code is unchanged by the commit operation; existing
validation and the three previously documented physics-suite failures remain
as recorded in the workspace migration plan.

## Status
Implemented; all twelve initial snapshots committed. Completed-plan metadata
recorded in separate documentation commits. No pushes or remotes were added.

## Implementation commit
`8c47f8feecf28acc718d3dff57e24a779318b124`


## Initial snapshot commits

These are the source baseline commits; later documentation-only commits record
plan metadata without changing these identifiers. Historical hashes already
written in older plans are retained as historical references.

| Repository | Initial snapshot |
|---|---|
| bullet_app | `cb6e3bf6e3ac7dbebd38e9ec28cd5575fce8759d` |
| bullet_drone | `ef298d68646e69d828a97df85dceb7a7a29ef18d` |
| bullet_msgs | `f496f5741f62ff42f8601984eff42db32a23cd29` |
| bullet_perception | `37acc3f5143eba681619cf78f6b75cf9f9ba81fd` |
| bullet_render | `d20705d5430f1555b1532a9cc7a931a05303303c` |
| bullet_view | `dd84b1a47ca5f5800f8a513dd04ca180f659289b` |
| bullet_visual | `90c0ec4eee373b24954799f835d0a23b381b067e` |
| flight_lens | `5e51cc00842e616742764aa7a884b18f9d31b9f3` |
| los_tracking | `9c788ee0cf169f6075dd5b1ec2a9ea70c671c791` |
| mcap_bagger | `48e4991889cee3f4425e3eb89e5e5606995ee624` |
| msp_link | `8652954381570c190823ad715514dca1da5e7076` |
| workspace | `8c47f8feecf28acc718d3dff57e24a779318b124` |

## Verification results

All twelve staged snapshots passed git diff --cached --check after removing
three extra EOF blank lines. No ignored project trees, caches, builds, environments
or recordings were staged. The existing configured identity was used unchanged.
Completed plans with Pending hashes now identify actual baseline commits, with
workspace-owned configuration/task changes explicitly attributed to the workspace.
Pending plans and existing historical commit references were not rewritten.
Final verification checks exact repository boundaries, clean status, main branches
and absent remotes. Runtime source was not changed, so the previous migration
verification and documented unrelated physics test failures remain applicable.
