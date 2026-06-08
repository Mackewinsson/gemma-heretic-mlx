#!/usr/bin/env python3
"""Interactive chat with viral-script system prompt and high temperature."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mlx_vlm.chat import MLXVisionChat  # noqa: E402
from rich import print as rprint  # noqa: E402
from rich.markdown import Markdown  # noqa: E402
from rich.panel import Panel  # noqa: E402
from rich.prompt import Prompt  # noqa: E402


DEFAULT_PROMPT = ROOT / "prompts" / "viral-system.txt"
HARDER_INSTRUCTION = (
    "HARDER: Rewrite your last answer 2x sharper. Zero disclaimers. "
    "Zero hedging. Maximum emotional punch. Hooks that start comment wars."
)


class ViralScriptChat(MLXVisionChat):
    def __init__(self, system_prompt: str, **kwargs):
        super().__init__(**kwargs)
        self.system_prompt = system_prompt.strip()
        if self.system_prompt:
            self.history.insert(
                0,
                {
                    "role": "system",
                    "content": [{"type": "text", "text": self.system_prompt}],
                },
            )

    def print_help(self) -> None:
        help_text = """
[bold yellow]Viral script mode[/bold yellow]
• Type a topic or brief — get hooks, angles, and scripts
• /harder — rewrite last answer sharper (no disclaimers)
• /image <path> — attach image
• /clear — clear history (keeps system prompt)
• /exit — quit
• /help — this message
        """
        rprint(Panel(help_text, title="Viral Chat", border_style="magenta"))
        rprint(
            f"[dim]temperature={self.temperature} max_tokens={self.max_tokens}[/dim]"
        )

    def handle_command(self, command: str, args: str) -> bool:
        if command == "/harder":
            if not self.history:
                rprint("[bold red]Nothing to rewrite yet.[/bold red]")
                return True
            self.add_to_history("user", HARDER_INSTRUCTION)
            response = self.generate_response()
            if not self.verbose:
                rprint(Panel(Markdown(response), border_style="green"))
            response = response.replace("<end_of_utterance>", "")
            self.add_to_history("assistant", response)
            return True
        if command == "/clear":
            self.history.clear()
            self.image_paths.clear()
            from mlx_vlm.generate import PromptCacheState

            self.prompt_cache_state = PromptCacheState()
            if self.system_prompt:
                self.history.insert(
                    0,
                    {
                        "role": "system",
                        "content": [{"type": "text", "text": self.system_prompt}],
                    },
                )
            rprint("[bold blue]History cleared. System prompt kept.[/bold blue]")
            return True
        return super().handle_command(command, args)


def load_system_prompt(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"System prompt not found: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Viral script chat (MLX VLM)")
    parser.add_argument("--model", default=os.environ.get("MODEL_ID"))
    parser.add_argument(
        "--system-prompt",
        type=Path,
        default=Path(os.environ.get("VIRAL_SYSTEM_PROMPT", DEFAULT_PROMPT)),
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=float(os.environ.get("VIRAL_TEMPERATURE", "0.95")),
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=int(os.environ.get("VIRAL_MAX_TOKENS", "1024")),
    )
    parser.add_argument("--verbose", action="store_true", default=False)
    args, _unknown = parser.parse_known_args()

    if not args.model:
        rprint("[bold red]Set MODEL_ID or pass --model[/bold red]")
        return 1

    system_prompt = load_system_prompt(args.system_prompt)
    chat = ViralScriptChat(
        system_prompt=system_prompt,
        model_path=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        verbose=args.verbose,
    )
    chat.chat_loop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
