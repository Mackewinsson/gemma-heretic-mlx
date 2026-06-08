#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$ROOT/scripts/common.sh"
ensure_setup

# shellcheck disable=SC1091
source "$ROOT/config.env"

VIRAL_TEMPERATURE="${VIRAL_TEMPERATURE:-0.95}"
VIRAL_MAX_TOKENS="${VIRAL_MAX_TOKENS:-1024}"
VIRAL_SYSTEM_PROMPT="${VIRAL_SYSTEM_PROMPT:-$ROOT/prompts/viral-system.txt}"

export VIRAL_TEMPERATURE VIRAL_MAX_TOKENS VIRAL_SYSTEM_PROMPT MODEL_ID

echo "Viral script mode | temperature=$VIRAL_TEMPERATURE | max_tokens=$VIRAL_MAX_TOKENS"
echo "Tip: type /harder after any reply to push it sharper."
echo ""

exec python "$ROOT/scripts/viral_chat.py" \
  --model "$MODEL_ID" \
  --system-prompt "$VIRAL_SYSTEM_PROMPT" \
  --temperature "$VIRAL_TEMPERATURE" \
  --max-tokens "$VIRAL_MAX_TOKENS" \
  "$@"
