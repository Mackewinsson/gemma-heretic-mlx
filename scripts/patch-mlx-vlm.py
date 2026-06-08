#!/usr/bin/env python3
"""Apply Gemma 4 MLX-format load fix to mlx-vlm (idempotent)."""

from __future__ import annotations

import sys
from pathlib import Path


PATCH_MARKER = "# MLX-format Gemma 4 checkpoints still ship KV-shared layer weights."
TARGET = "            if hasattr(model_class, \"AudioModel\"):"
INSERT_AFTER_BLOCK = """    elif config.get("model_type") == "gemma4" and hasattr(
        model_class, "LanguageModel"
    ):
        # MLX-format Gemma 4 checkpoints still ship KV-shared layer weights.
        weights = sanitize_weights(
            model_class.LanguageModel, weights, model_config.text_config
        )
"""


def find_utils_py(venv_dir: Path) -> Path:
    candidates = list(
        venv_dir.glob("lib/python*/site-packages/mlx_vlm/utils.py")
    )
    if not candidates:
        raise FileNotFoundError(
            f"mlx_vlm not found under {venv_dir}. Run ./setup.sh first."
        )
    return candidates[0]


def main() -> int:
    venv_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "venv").resolve()
    utils_py = find_utils_py(venv_dir)
    text = utils_py.read_text()

    if PATCH_MARKER in text:
        print(f"Already patched: {utils_py}")
        return 0

    if TARGET not in text:
        raise RuntimeError(
            f"Unexpected mlx-vlm version; cannot patch {utils_py}. "
            "Update scripts/patch-mlx-vlm.py for your mlx-vlm version."
        )

    # Insert after the AudioModel sanitize block (before `if not has_quantization:`).
    anchor = (
        "            if hasattr(model_class, \"AudioModel\"):\n"
        "                weights = sanitize_weights(\n"
        "                    model_class.AudioModel, weights, model_config.audio_config\n"
        "                )\n"
        "\n"
        "    if not has_quantization:"
    )
    replacement = (
        "            if hasattr(model_class, \"AudioModel\"):\n"
        "                weights = sanitize_weights(\n"
        "                    model_class.AudioModel, weights, model_config.audio_config\n"
        "                )\n"
        + INSERT_AFTER_BLOCK
        + "\n"
        "    if not has_quantization:"
    )

    if anchor not in text:
        raise RuntimeError(f"Patch anchor not found in {utils_py}")

    utils_py.write_text(text.replace(anchor, replacement, 1))
    print(f"Patched: {utils_py}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
