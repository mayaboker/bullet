# Publish workspace and projects on GitHub

## Goal
Create public GitHub repositories for the workspace and all eleven projects and
push each current main branch, as explicitly requested by the user.

## Implementation
- Verify GitHub authentication, repository-name availability and clean local
  main branches. Use authenticated owner mayaboker and current directory names:
  bullet for the workspace and each projects/<name> name for its project.
- Create twelve public repositories without generated README/license commits.
  Add origin and push the existing local history with main tracking origin/main.
- Document repository links and verify public visibility, exact remote commit
  identity, clean working trees and upstream branches. Commit/push workspace
  publication documentation, recording actual implementation hashes separately.

## Defaults and interfaces
No submodules, force pushes, history rewrites or private repositories. Do not
upload ignored projects through the workspace, recordings, environments or build
outputs. Preserve separate histories. Repository creation/push uses authenticated
GitHub CLI because connected tools do not provide repository creation/local push.

## Verification
Authenticated owner and all twelve names checked through GitHub API; all names
were available. Verify API private=false, default_branch=main, git ls-remote main
matching each local HEAD, origin/main tracking and clean status after publishing.

## Status
Partially published: ten project repositories are public and pushed. GitHub
repository-creation rate limiting blocks bullet and msp_link. Do not mark complete
until both are created/pushed and every remote is verified.

## Implementation commit
`e3ad2d05f0072f99e136e2c9125c88e2da415d28` (workspace publication documentation)


## Publication results

Ten projects were created through gh repo create --public --source --remote
origin --push. GitHub API confirmed public visibility and main as default branch;
git ls-remote confirmed each main SHA equals its local HEAD. All ten main branches
track origin/main. GitHub creation errors prevented origin creation for bullet and
msp_link; retries after cooldowns returned the same external service error.
No force pushes or history rewrites were used.

Verified public projects: bullet_app, bullet_drone, bullet_msgs, bullet_perception,
bullet_render, bullet_view, bullet_visual, flight_lens, los_tracking, mcap_bagger.
Machine-readable verification: /tmp/bullet-github-verified-projects.json.

## Resume after GitHub allows repository creation

From the workspace root, create and push the remaining repositories:

```bash
gh repo create mayaboker/bullet --public --source . --remote origin --push
gh repo create mayaboker/msp_link --public --source projects/msp_link --remote origin --push
```

Then verify public visibility and remote/local SHA equality, update the repository
status table and this plan, commit those workspace documentation updates and push
the final workspace main. Recheck remote existence before retrying if GitHub state
has changed; never overwrite an existing repository or force push.
