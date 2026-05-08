#!/usr/bin/env bash
# deploy.sh -- rebuild and redeploy bot container
#
# Usage:
#   chmod +x scripts/deploy.sh
#   ./scripts/deploy.sh
#
# Optional overrides:
#   IMAGE_NAME=mybot CONTAINER_NAME=mybot_c APP_DIR=/root/learning ./deploy.sh

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

IMAGE_NAME="${IMAGE_NAME:-testbot}"
CONTAINER_NAME="${CONTAINER_NAME:-testbot_c}"
APP_DIR="${APP_DIR:-${PROJECT_ROOT}}"
DOCKERFILE_PATH="${DOCKERFILE_PATH:-${PROJECT_ROOT}/dockerfile}"

echo "=== Deploy starting ==="
echo "App dir: ${APP_DIR}"
echo "Image:   ${IMAGE_NAME}:latest"
echo "Container: ${CONTAINER_NAME}"

cd "${APP_DIR}"

if [[ ! -f "${DOCKERFILE_PATH}" ]]; then
  echo "Dockerfile path '${DOCKERFILE_PATH}' not found." >&2
  echo "Set DOCKERFILE_PATH=/absolute/path/to/dockerfile if needed." >&2
  exit 1
fi

echo "=== Building image ==="
docker build -f "${DOCKERFILE_PATH}" -t "${IMAGE_NAME}:latest" "${APP_DIR}"

echo "=== Replacing container (if exists) ==="
if docker ps -a --format '{{.Names}}' | grep -qx "${CONTAINER_NAME}"; then
  docker rm -f "${CONTAINER_NAME}" >/dev/null
fi

echo "=== Starting container ==="
docker run -d --name "${CONTAINER_NAME}" --restart unless-stopped "${IMAGE_NAME}:latest" >/dev/null

echo "=== Deployment complete ==="
docker ps --filter "name=${CONTAINER_NAME}" --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}'
echo
echo "Recent logs:"
docker logs --tail 20 "${CONTAINER_NAME}" || true
