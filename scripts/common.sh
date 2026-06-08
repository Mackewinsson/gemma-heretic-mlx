#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$ROOT/venv"

if [[ -f "$ROOT/config.env" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT/config.env"
fi

MODEL_ID="${MODEL_ID:-deadbydawn101/gemma-4-E2B-Heretic-Uncensored-mlx-4bit}"
SERVER_PORT="${SERVER_PORT:-8080}"

activate_venv() {
  if [[ ! -d "$VENV" ]]; then
    echo "Virtualenv not found. Run: $ROOT/setup.sh" >&2
    exit 1
  fi
  # shellcheck disable=SC1091
  source "$VENV/bin/activate"
}

ensure_setup() {
  activate_venv
  if ! python -c "import mlx_vlm" 2>/dev/null; then
    echo "mlx-vlm missing. Run: $ROOT/setup.sh" >&2
    exit 1
  fi
}
