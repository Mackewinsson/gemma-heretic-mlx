#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$ROOT/scripts/common.sh"
ensure_setup

exec mlx_vlm.chat --model "$MODEL_ID" "$@"
