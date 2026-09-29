"""Voice backends — LATER MODULE.

Trace order after the text agent already works:
  1. voice/base.py       — the Speak protocol (one method)
  2. voice/macos_say.py  — free local practice voice (robotic, fine for wiring)
  3. voice/elevenlabs_tts.py — cinematic quality (API key)
  4. voice/grok_tts.py    — xAI / Grok Speech TTS (API key)
  5. lessons/04_voice_speak.py — bolt speak() onto agent.ask()

Honest tradeoff Frank will care about:
  - The LLM stays 100% local.
  - "Really really good" voices (ElevenLabs, Grok) leave the machine as text,
    come back as audio. That's the deal for studio-quality TTS in 2026.
  - Fully-local voices exist (macOS `say`, Piper, mlx-audio) but they won't
    sound like ElevenLabs. Use them to learn the plumbing first.
"""

from .base import Speaker, make_speaker

__all__ = ["Speaker", "make_speaker"]
