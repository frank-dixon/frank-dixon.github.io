"""Agent loop tests against FakeBrain — no network, no GPU."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nano_agent.agent import Agent
from nano_agent.config import Settings
from nano_agent.voice.file_stub import FileStubSpeaker


def test_mock_agent_answers(monkeypatch, tmp_path) -> None:
    # Avoid a real DuckDuckGo hit during the mock search round.
    import nano_agent.agent as agent_mod

    monkeypatch.setattr(
        agent_mod,
        "search_web",
        lambda query, max_results=5: f"1. Fake hit for {query}\n   stub body",
    )

    settings = Settings(mock=True, max_tool_rounds=3)
    agent = Agent(settings=settings)
    answer = agent.ask("What is happening with Python lately?")
    assert "mock reply" in answer.lower() or "search results" in answer.lower()


def test_file_stub_speaker(tmp_path) -> None:
    speaker = FileStubSpeaker(out_dir=tmp_path)
    status = speaker.speak("hello from tests")
    assert "wrote" in status
    assert (tmp_path / "last_utterance.txt").read_text() == "hello from tests\n"
