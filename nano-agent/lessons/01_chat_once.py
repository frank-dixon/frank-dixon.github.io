#!/usr/bin/env python3
"""Lesson 01 — talk to a local model ONCE. No agent. No tools.

Goal: prove Ollama is alive and you understand one chat round-trip.

  cd nano-agent
  pip install -r requirements.txt
  ollama pull llama3.2:1b
  python lessons/01_chat_once.py
  NANO_MOCK=1 python lessons/01_chat_once.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow `python lessons/01_chat_once.py` without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nano_agent.config import load_settings
from nano_agent.llm import make_brain


def main() -> None:
    settings = load_settings()
    brain = make_brain(settings)
    messages = [
        {"role": "system", "content": "Reply in one short sentence."},
        {"role": "user", "content": "What is 2 + 2?"},
    ]
    print(f"model={settings.model!r} mock={settings.mock}")
    print("---")
    print(brain.chat(messages))


if __name__ == "__main__":
    main()
