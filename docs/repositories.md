# Public GitHub repositories

The workspace and projects are independent public repositories owned by
[`mayaboker`](https://github.com/mayaboker). Each local repository uses its own
`origin` remote, with `main` tracking `origin/main`. There are no submodules.

| Local directory | GitHub repository |
|---|---|
| Workspace root | [bullet](https://github.com/mayaboker/bullet) |
| `projects/bullet_app` | [bullet_app](https://github.com/mayaboker/bullet_app) |
| `projects/bullet_drone` | [bullet_drone](https://github.com/mayaboker/bullet_drone) |
| `projects/bullet_msgs` | [bullet_msgs](https://github.com/mayaboker/bullet_msgs) |
| `projects/bullet_perception` | [bullet_perception](https://github.com/mayaboker/bullet_perception) |
| `projects/bullet_render` | [bullet_render](https://github.com/mayaboker/bullet_render) |
| `projects/bullet_view` | [bullet_view](https://github.com/mayaboker/bullet_view) |
| `projects/bullet_visual` | [bullet_visual](https://github.com/mayaboker/bullet_visual) |
| `projects/flight_lens` | [flight_lens](https://github.com/mayaboker/flight_lens) |
| `projects/los_tracking` | [los_tracking](https://github.com/mayaboker/los_tracking) |
| `projects/mcap_bagger` | [mcap_bagger](https://github.com/mayaboker/mcap_bagger) |
| `projects/msp_link` | [msp_link](https://github.com/mayaboker/msp_link) |

## Clone the complete workspace

Cloning the workspace alone does not fetch its ignored project directories.
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
