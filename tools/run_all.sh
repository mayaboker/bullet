#!/usr/bin/env bash
set -euo pipefail

workspace_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
flight_profile=${1:?flight profile is required}
drone_model=${2:?drone model is required}
case "$flight_profile:$drone_model" in
  internal:racer) physics_profile=internal.yaml; mission_profile=bullet_profile.yaml ;;
  betaflight:racer) physics_profile=betaflight.yaml; mission_profile=betaflight_los.yaml ;;
  internal:heavy_quad) physics_profile=internal_heavy_quad.yaml; mission_profile=bullet_profile_heavy_quad.yaml ;;
  betaflight:heavy_quad) physics_profile=betaflight_heavy_quad.yaml; mission_profile=betaflight_los_heavy_quad.yaml ;;
  *) echo "Unknown backend/drone combination: $flight_profile:$drone_model" >&2; exit 2 ;;
esac
cd "$workspace_root"
uv run --locked --all-packages python tools/cleanup_flight.py
(cd projects/bullet_render && cmake --preset debug && cmake --build --preset debug)
uv run --locked --package bullet-view bullet-view &
bullet_view_pid=$!
uv run --locked --package bullet-visual bullet-visual --config "$workspace_root/projects/bullet_visual/config/zmq.yaml" &
bullet_visual_pid=$!
cleanup() {
  kill "$bullet_visual_pid" "$bullet_view_pid" 2>/dev/null || true
}
trap cleanup EXIT
uv run --locked --all-packages --all-extras --all-groups python "$workspace_root/tools/run_flight.py" \
  --physics-config "$workspace_root/config/$physics_profile" \
  --mission-config "$workspace_root/config/$mission_profile" \
  --controls-config "$workspace_root/config/operator_controls.yaml" \
  --mcap-output-dir "$workspace_root/recordings"
