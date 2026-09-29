"""xAI Grok Speech TTS — the other "damn that sounds good" option.

Needs:
  export XAI_API_KEY=...

Manual curl equivalent:
  curl -X POST https://api.x.ai/v1/tts \\
    -H "Authorization: Bearer $XAI_API_KEY" \\
    -H "Content-Type: application/json" \\
    -d '{"text":"Hello from Grok voice","voice_id":"eve","language":"en"}' \\
    --output out.mp3

Docs: https://docs.x.ai/developers/model-capabilities/audio/text-to-speech
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import httpx


class GrokSpeaker:
    name = "grok"

    def __init__(
        self,
        voice_id: str | None = None,
        language: str | None = None,
        out_dir: str | Path | None = None,
    ) -> None:
        self.api_key = os.getenv("XAI_API_KEY", "").strip()
        self.voice_id = voice_id or os.getenv("XAI_VOICE_ID", "eve").strip()
        self.language = language or os.getenv("XAI_TTS_LANGUAGE", "en").strip()
        self.out_dir = Path(out_dir or Path.cwd() / ".nano_agent_audio")
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.url = os.getenv("XAI_TTS_URL", "https://api.x.ai/v1/tts").strip()

    def speak(self, text: str) -> str:
        text = (text or "").strip()
        if not text:
            return "skipped: empty text"
        if not self.api_key:
            raise RuntimeError(
                "XAI_API_KEY is not set. "
                "Get one at https://console.x.ai and export it."
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "voice_id": self.voice_id,
            "language": self.language,
        }
        with httpx.Client(timeout=120.0) as client:
            resp = client.post(self.url, headers=headers, json=payload)
            if resp.status_code >= 400:
                raise RuntimeError(
                    f"Grok TTS failed ({resp.status_code}): {resp.text[:500]}"
                )
            raw = resp.content

        out_path = self.out_dir / "grok_last.mp3"
        out_path.write_bytes(raw)
        _try_play_mp3(out_path)
        return f"saved {out_path} ({len(raw)} bytes)"


def _try_play_mp3(path: Path) -> None:
    if shutil.which("afplay"):
        subprocess.run(["afplay", str(path)], check=False)
        return
    if shutil.which("ffplay"):
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", str(path)],
            check=False,
        )
