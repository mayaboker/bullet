# Public GitHub repositories

The projects are published as independent public repositories owned by
[`mayaboker`](https://github.com/mayaboker). Each published local repository uses its own
`origin` remote, with `main` tracking `origin/main`. There are no submodules.

Ten project repositories are public and pushed. GitHub temporarily rejected
creation of `bullet` and `msp_link` with "You have created too many repositories,
too quickly. Please try again later." Those two repositories remain local and
committed, without origins. Their creation/push is pending.


| Local directory | GitHub repository | Status |
|---|---|---|
| Workspace root | [bullet](https://github.com/mayaboker/bullet)  Pending creation |
| `projects/bullet_app` | [bullet_app](https://github.com/mayaboker/bullet_app)  Public; pushed |
| `projects/bullet_drone` | [bullet_drone](https://github.com/mayaboker/bullet_drone)  Public; pushed |
| `projects/bullet_msgs` | [bullet_msgs](https://github.com/mayaboker/bullet_msgs)  Public; pushed |
| `projects/bullet_perception` | [bullet_perception](https://github.com/mayaboker/bullet_perception)  Public; pushed |
| `projects/bullet_render` | [bullet_render](https://github.com/mayaboker/bullet_render)  Public; pushed |
| `projects/bullet_view` | [bullet_view](https://github.com/mayaboker/bullet_view)  Public; pushed |
| `projects/bullet_visual` | [bullet_visual](https://github.com/mayaboker/bullet_visual)  Public; pushed |
| `projects/flight_lens` | [flight_lens](https://github.com/mayaboker/flight_lens)  Public; pushed |
| `projects/los_tracking` | [los_tracking](https://github.com/mayaboker/los_tracking)  Public; pushed |
| `projects/mcap_bagger` | [mcap_bagger](https://github.com/mayaboker/mcap_bagger)  Public; pushed |
| `projects/msp_link` | [msp_link](https://github.com/mayaboker/msp_link)  Pending creation |

## Clone the complete workspace

Once the two pending repositories have been created, the following clones the
complete workspace. Cloning the workspace alone does not fetch its ignored project directories.
Clone each project separately:

```bash
git clone https://github.com/mayaboker/bullet.git
cd bullet
mkdir -p projects
for project in bullet_app bullet_drone bullet_msgs bullet_perception bullet_render bullet_view bullet_visual flight_lens los_tracking mcap_bagger msp_link; do
  git clone "https://github.com/mayaboker/$project.git" "projects/$project"
done
uv sync --locked --all-packages --all-extras --all-groups
```

## Publish later changes

Commit and push workspace changes from the workspace root. Commit and push each
project's changes from its own directory. A workspace push does not publish
changes in the project repositories. Generated recordings, environments and
build outputs remain ignored.

See [project ownership](project-structure.md#git-ownership) and the
[publication plan](../plan/0004-public-github-repositories.md).
