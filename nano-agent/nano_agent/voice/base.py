"""Shared Speaker protocol + factory.

Manual mental model:
  answer = agent.ask(question)   # text, local
  speaker.speak(answer)          # audio, local OR cloud

Swap speakers without touching the agent. That's the whole point of a Protocol.
"""

from __future__ import annotations

import os
from typing import Protocol


class Speaker(Protocol):
    """Anything that can turn text into sound (or a saved audio file)."""

    name: str

    def speak(self, text: str) -> str:
        """Speak `text`. Returns a short status string (path or 'played')."""
        ...


def make_speaker(backend: str | None = None) -> Speaker:
    """Pick a voice backend from an explicit name or NANO_VOICE env var.

    Backends:
      say         — macOS `say` (default on Darwin; great for learning)
      elevenlabs  — ElevenLabs TTS (needs ELEVENLABS_API_KEY)
      grok        — xAI Grok Speech TTS (needs XAI_API_KEY)
      file        — write a .txt stub path (CI / no audio devices)
    """
    choice = (backend or os.getenv("NANO_VOICE", "")).strip().lower()
    if not choice:
        # Sensible default: local practice voice on Mac, file stub elsewhere.
        import sys

        choice = "say" if sys.platform == "darwin" else "file"

    if choice in {"say", "macos", "macos_say"}:
        from .macos_say import MacSaySpeaker

        return MacSaySpeaker()
    if choice in {"eleven", "elevenlabs", "11labs"}:
        from .elevenlabs_tts import ElevenLabsSpeaker

        return ElevenLabsSpeaker()
    if choice in {"grok", "xai", "grok_tts"}:
        from .grok_tts import GrokSpeaker

        return GrokSpeaker()
    if choice in {"file", "stub", "none"}:
        from .file_stub import FileStubSpeaker

        return FileStubSpeaker()

    raise ValueError(
        f"Unknown voice backend {choice!r}. "
        "Use: say | elevenlabs | grok | file"
    )
