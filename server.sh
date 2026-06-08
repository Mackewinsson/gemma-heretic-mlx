#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$ROOT/scripts/common.sh"
ensure_setup

echo "OpenAI-compatible API: http://localhost:${SERVER_PORT}/v1"
echo "Model ID for Cursor:   $MODEL_ID"
echo "Press Ctrl+C to stop."
echo ""

exec mlx_vlm.server --model "$MODEL_ID" --port "$SERVER_PORT" "$@"
