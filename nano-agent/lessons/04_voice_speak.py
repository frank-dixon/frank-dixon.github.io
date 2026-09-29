#!/usr/bin/env python3
"""Lesson 04 — LATER MODULE: bolt a voice onto the text agent (CLI only).

Do this AFTER lessons 01–03 feel boring. Text first. Ego second. Voice third.

Practice wiring (free, robotic on Mac):
  NANO_MOCK=1 NANO_VOICE=say python lessons/04_voice_speak.py "say hello"

Cloud quality (API key required):
  NANO_MOCK=1 NANO_VOICE=elevenlabs python lessons/04_voice_speak.py "hello"
  NANO_MOCK=1 NANO_VOICE=grok python lessons/04_voice_speak.py "hello"

Or via the main CLI:
  python -m nano_agent --speak --voice elevenlabs "Summarize today's AI news"
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nano_agent.agent import Agent
from nano_agent.config import load_settings
from nano_agent.voice import make_speaker


def main() -> None:
    question = " ".join(sys.argv[1:]) or "Say a one-sentence hello."
    settings = load_settings()
    agent = Agent(settings=settings, trace=lambda m: print(m, file=sys.stderr))
    speaker = make_speaker()  # NANO_VOICE / platform default

    print(f"voice backend: {speaker.name}", file=sys.stderr)
    answer = agent.ask(question)
    print("--- final text ---")
    print(answer)
    print("--- speak ---")
    print(speaker.speak(answer))


if __name__ == "__main__":
    main()
