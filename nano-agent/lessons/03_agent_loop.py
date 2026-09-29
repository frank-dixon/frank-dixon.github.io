#!/usr/bin/env python3
"""Lesson 03 — glue brain + search into the agent loop.

This is the same loop as `python -m nano_agent`, printed with full trace.

  cd nano-agent
  NANO_MOCK=1 python lessons/03_agent_loop.py "what's new in python?"
  python lessons/03_agent_loop.py "capital of France"   # needs Ollama
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nano_agent.agent import Agent
from nano_agent.config import load_settings


def main() -> None:
    question = " ".join(sys.argv[1:]) or "What is a local LLM?"
    settings = load_settings()
    agent = Agent(settings=settings, trace=lambda m: print(m, file=sys.stderr))
    print("--- final ---")
    print(agent.ask(question))


if __name__ == "__main__":
    main()
