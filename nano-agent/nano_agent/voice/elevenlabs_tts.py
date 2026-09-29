"""ElevenLabs TTS — the "holy shit that sounds real" option.

Needs:
  pip install elevenlabs
  export ELEVENLABS_API_KEY=...

Manual curl equivalent (approx):
  curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/VOICE_ID" \\
    -H "xi-api-key: $ELEVENLABS_API_KEY" \\
    -H "Content-Type: application/json" \\
    -d '{"text":"Hello","model_id":"eleven_multilingual_v2"}' \\
    --output out.mp3

Docs: https://elevenlabs.io/docs
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


class ElevenLabsSpeaker:
    name = "elevenlabs"

    def __init__(
        self,
        voice_id: str | None = None,
        model_id: str | None = None,
        out_dir: str | Path | None = None,
    ) -> None:
        self.api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
        # Default public demo voice id from ElevenLabs docs (Rachel-ish / JB).
        self.voice_id = (
            voice_id
            or os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb").strip()
        )
        self.model_id = (
            model_id
            or os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2").strip()
        )
        self.out_dir = Path(out_dir or Path.cwd() / ".nano_agent_audio")
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def speak(self, text: str) -> str:
        text = (text or "").strip()
        if not text:
            return "skipped: empty text"
        if not self.api_key:
            raise RuntimeError(
                "ELEVENLABS_API_KEY is not set. "
                "Get one at https://elevenlabs.io and export it."
            )

        try:
            from elevenlabs.client import ElevenLabs
        except ImportError as exc:
            raise RuntimeError(
                "Install the optional voice extra:\n"
                "  pip install 'elevenlabs>=1.50.0'"
            ) from exc

        client = ElevenLabs(api_key=self.api_key)
        # convert() yields / returns audio bytes depending on SDK version —
        # normalize to bytes either way.
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=self.voice_id,
            model_id=self.model_id,
            output_format="mp3_44100_128",
        )
        raw = _coerce_audio_bytes(audio)

        out_path = self.out_dir / "elevenlabs_last.mp3"
        out_path.write_bytes(raw)
        _try_play_mp3(out_path)
        return f"saved {out_path} ({len(raw)} bytes)"


def _coerce_audio_bytes(audio: object) -> bytes:
    if isinstance(audio, (bytes, bytearray)):
        return bytes(audio)
    # Newer SDKs return an iterator of chunks.
    chunks: list[bytes] = []
    for chunk in audio:  # type: ignore[attr-defined]
        if isinstance(chunk, (bytes, bytearray)):
            chunks.append(bytes(chunk))
    return b"".join(chunks)


def _try_play_mp3(path: Path) -> None:
    """Best-effort local playback from CLI — no GUI players required."""
    if shutil.which("afplay"):  # macOS
        subprocess.run(["afplay", str(path)], check=False)
        return
    if shutil.which("ffplay"):
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", str(path)],
            check=False,
        )
