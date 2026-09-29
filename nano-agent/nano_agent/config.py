"""Knobs you can change without digging through the agent loop.

On a MacBook you typically:
  1. Install Ollama from https://ollama.com
  2. `ollama pull llama3.2:1b`   (nano — ~1.3 GB, great for learning)
  3. Or `ollama pull llama3.2`   (micro — 3B, still friendly on 8–16 GB)
  4. Leave Ollama running; this app talks to http://127.0.0.1:11434
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # Ollama's default local OpenAI-compatible-ish chat endpoint lives here.
    # We use the native /api/chat route — simpler than the OpenAI shim.
    ollama_host: str = os.getenv("NANO_OLLAMA_HOST", "http://127.0.0.1:11434")

    # Tiny models that fit a MacBook without drama. Override with NANO_MODEL.
    # Good "nano" picks:  llama3.2:1b, gemma2:2b, qwen2.5:1.5b
    # Good "micro" picks: llama3.2 (3B), phi3:mini, gemma2:9b (needs more RAM)
    model: str = os.getenv("NANO_MODEL", "llama3.2:1b")

    # Cap how many tool round-trips we allow so a confused model can't loop forever.
    max_tool_rounds: int = int(os.getenv("NANO_MAX_TOOL_ROUNDS", "3"))

    # How many DuckDuckGo hits to feed back into the model.
    search_max_results: int = int(os.getenv("NANO_SEARCH_MAX_RESULTS", "5"))

    # When True, never hit Ollama — use a scripted FakeBrain (see llm.py).
    # Great for tracing the agent loop offline / in CI / on a machine with no model.
    mock: bool = os.getenv("NANO_MOCK", "").lower() in {"1", "true", "yes"}


def load_settings() -> Settings:
    return Settings()
