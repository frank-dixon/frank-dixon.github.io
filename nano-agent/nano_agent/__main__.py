"""CLI entrypoint — 100% terminal, zero GUI.

Run from the nano-agent folder:

  python -m nano_agent "What is the capital of France?"
  NANO_MOCK=1 python -m nano_agent "latest python release"
  python -m nano_agent --speak --voice say "Tell me a one-line joke"
  python -m nano_agent --speak --voice elevenlabs "Who won the Oscars?"
  python -m nano_agent --speak --voice grok "Explain local LLMs briefly"
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import replace

from .agent import Agent
from .config import load_settings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="nano_agent",
        description=(
            "Tiny local LLM agent with optional DuckDuckGo search + optional TTS. "
            "CLI only — no GUI."
        ),
    )
    parser.add_argument(
        "question",
        nargs="?",
        help="Your question. If omitted, reads one line from stdin.",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use FakeBrain (no Ollama). Same as NANO_MOCK=1.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Hide the think/search trace; only print the final answer.",
    )
    parser.add_argument(
        "--speak",
        action="store_true",
        help="Speak the final answer via the chosen voice backend (still CLI).",
    )
    parser.add_argument(
        "--voice",
        choices=("say", "elevenlabs", "grok", "file"),
        default=None,
        help=(
            "TTS backend when --speak is set. "
            "Default: macOS say on Mac, file stub elsewhere. "
            "elevenlabs needs ELEVENLABS_API_KEY; grok needs XAI_API_KEY."
        ),
    )
    args = parser.parse_args(argv)

    settings = load_settings()
    if args.mock:
        settings = replace(settings, mock=True)

    question = args.question
    if not question:
        question = sys.stdin.readline()
    if not question or not question.strip():
        parser.error("pass a question as an argument, or pipe one on stdin")

    def trace(msg: str) -> None:
        if not args.quiet:
            print(msg, file=sys.stderr)

    agent = Agent(settings=settings, trace=trace)
    try:
        answer = agent.ask(question)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(answer)

    if args.speak:
        from .voice import make_speaker

        try:
            speaker = make_speaker(args.voice)
            status = speaker.speak(answer)
        except RuntimeError as exc:
            print(f"voice error: {exc}", file=sys.stderr)
            return 2
        if not args.quiet:
            print(f"[voice:{speaker.name}] {status}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
