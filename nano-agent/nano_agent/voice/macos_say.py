"""Free practice voice: macOS built-in `say`.

Sounds like a GPS from 2009. Perfect. Learn the SPEAK wiring here,
then swap to ElevenLabs / Grok when you want it to sound human.

Manual equivalent:
  say -v Samantha "Hello from the nano agent"
"""

from __future__ import annotations

import shutil
import subprocess
import sys


class MacSaySpeaker:
    name = "macos_say"

    def __init__(self, voice: str | None = None) -> None:
        # Common decent Mac voices: Samantha, Alex, Daniel, Karen, Moira
        self.voice = voice or "Samantha"

    def speak(self, text: str) -> str:
        text = (text or "").strip()
        if not text:
            return "skipped: empty text"

        if sys.platform != "darwin":
            return (
                "skipped: macOS `say` only works on Darwin. "
                "Use NANO_VOICE=file here, or elevenlabs/grok for cloud TTS."
            )
        if shutil.which("say") is None:
            return "skipped: `say` binary not found on PATH"

        cmd = ["say", "-v", self.voice, text]
        subprocess.run(cmd, check=True)
        return f"played via say -v {self.voice}"
