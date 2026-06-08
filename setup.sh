#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/venv"

echo "==> Gemma Heretic MLX setup"
echo "    Project: $ROOT"

if [[ ! -d "$VENV" ]]; then
  echo "==> Creating virtualenv..."
  python3 -m venv "$VENV"
fi

# shellcheck disable=SC1091
source "$VENV/bin/activate"
python -m pip install --upgrade pip
python -m pip install mlx-vlm huggingface_hub

echo "==> Applying mlx-vlm Gemma 4 patch..."
python "$ROOT/scripts/patch-mlx-vlm.py" "$VENV"

echo ""
echo "Done. Run chat with:"
echo "  $ROOT/chat.sh"
