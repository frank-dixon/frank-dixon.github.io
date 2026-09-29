"""CI / Linux stub — writes text to a .txt "audio" stand-in.

Use this when you have no speakers, no Mac, and no API keys.
Proves the agent → speaker handoff without making noise.
"""

from __future__ import annotations

from pathlib import Path


class FileStubSpeaker:
    name = "file_stub"

    def __init__(self, out_dir: str | Path | None = None) -> None:
        self.out_dir = Path(out_dir or Path.cwd() / ".nano_agent_audio")
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def speak(self, text: str) -> str:
        text = (text or "").strip()
        if not text:
            return "skipped: empty text"
        path = self.out_dir / "last_utterance.txt"
        path.write_text(text + "\n", encoding="utf-8")
        return f"wrote {path}"
