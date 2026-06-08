# Gemma 4 E2B Heretic — MLX local chat (Apple Silicon)

Run **Gemma-4-E2B-Heretic-Uncensored** locally on Mac (~3.34 GB, MLX 4-bit).

Model: [deadbydawn101/gemma-4-E2B-Heretic-Uncensored-mlx-4bit](https://huggingface.co/deadbydawn101/gemma-4-E2B-Heretic-Uncensored-mlx-4bit)

## Quick start

```bash
cd ~/Projects/gemma-heretic-mlx
./setup.sh    # once
./chat.sh     # terminal chat
```

## Scripts

| Script | What it does |
|--------|----------------|
| `./setup.sh` | Creates `venv`, installs `mlx-vlm`, applies Gemma 4 load fix |
| `./chat.sh` | Interactive terminal chat |
| `./server.sh` | OpenAI-compatible API on port 8080 (for Cursor) |
| `./ui.sh` | Web chat UI in browser (installs Gradio on first run) |

## Cursor

1. `./server.sh`
2. **Cursor → Settings → Models**
   - OpenAI API Key: `mlx`
   - Override OpenAI Base URL: `http://localhost:8080/v1`
   - Model: `deadbydawn101/gemma-4-E2B-Heretic-Uncensored-mlx-4bit`
3. Chat with `Cmd+L`

If Cursor rejects `localhost`, tunnel with ngrok: `ngrok http 8080` and use `https://….ngrok-free.app/v1`.

## Chat commands

- `/help` — help
- `/clear` — clear history
- `/image <path>` — attach an image (multimodal)
- `/exit` — quit

## Requirements

- macOS with Apple Silicon (M1/M2/M3/M4)
- ~8 GB free RAM recommended (16 GB Mac works well)
- Python 3.11+ (3.14 tested)

## Optional: faster Hugging Face downloads

```bash
export HF_TOKEN="hf_…"   # https://huggingface.co/settings/tokens
./setup.sh
```

## What the patch does

MLX-format Gemma 4 checkpoints include extra KV-shared layer weights. `mlx-vlm` skips sanitization for MLX files, which causes a load error. `scripts/patch-mlx-vlm.py` fixes that automatically during setup.
