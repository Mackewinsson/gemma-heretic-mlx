#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$ROOT/scripts/common.sh"
ensure_setup

if ! python -c "import gradio" 2>/dev/null; then
  echo "Installing web UI dependencies..."
  pip install 'mlx-vlm[ui]'
fi

exec mlx_vlm.chat_ui --model "$MODEL_ID" "$@"
