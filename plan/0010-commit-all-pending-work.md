# Commit all pending workspace and project work

- Status: In progress
- Implementation commit: Pending

Commit the authorized pending work separately in the workspace, bullet_app,
bullet_bringup, bullet_drone, bullet_msgs, bullet_render, bullet_view and
mcap_bagger repositories. Preserve independent Git boundaries, do not add
submodules, and leave the five clean repositories unchanged. Include the existing
bringup, manual flight/recording, collision gating, state-based buttons and MSP
schema repair changes. Do not push.

Check staged whitespace, lock consistency and staged source/config/documentation
contents. Prior implementation plans contain test/build/MCAP verification results.
After implementation commits exist, record their actual hashes in affected plans
and menus in separate documentation commits; verify all repositories finish clean.
