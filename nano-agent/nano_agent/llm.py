"""The 'brain' — send chat messages to a local model, get text back.

Manual equivalent if you were doing this in a terminal:

  curl http://127.0.0.1:11434/api/chat -d '{
    "model": "llama3.2:1b",
    "messages": [{"role": "user", "content": "hi"}],
    "stream": false
  }'

That's literally all this file wraps. If you can curl it, you can build it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

import httpx

from .config import Settings


# A chat turn. Roles match what every chat model expects:
#   system = instructions, user = you, assistant = the model,
#   tool    = result of a tool we ran (we stuff it in as a user message
#             for tiny models that don't have native tool APIs yet).
Message = dict[str, str]


class Brain(Protocol):
    """Anything that can reply to a message list. Lets us swap real ↔ mock."""

    def chat(self, messages: list[Message]) -> str: ...


@dataclass
class OllamaBrain:
    """Talks to a running Ollama daemon on your Mac."""

    settings: Settings
    timeout: float = 120.0

    def chat(self, messages: list[Message]) -> str:
        url = f"{self.settings.ollama_host.rstrip('/')}/api/chat"
        payload: dict[str, Any] = {
            "model": self.settings.model,
            "messages": messages,
            "stream": False,  # one full reply; streaming is a later lesson
            "options": {
                # Keep creativity low — we want reliable JSON tool calls.
                "temperature": 0.2,
            },
        }
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
        except httpx.ConnectError as exc:
            raise RuntimeError(
                "Could not reach Ollama at "
                f"{self.settings.ollama_host}.\n"
                "Install from https://ollama.com then run:\n"
                f"  ollama pull {self.settings.model}\n"
                "Or retrace the loop without a model:\n"
                "  NANO_MOCK=1 python -m nano_agent \"What's new with Python?\""
            ) from exc

        # Ollama returns: {"message": {"role": "assistant", "content": "..."}, ...}
        message = data.get("message") or {}
        content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError(f"Ollama returned an empty reply: {data!r}")
        return content.strip()


@dataclass
class FakeBrain:
    """Scripted replies so you can practice the agent loop with zero GPU/RAM.

    First call → asks to search. Second call → answers from the tool result.
    That's the whole agent pattern in two lines of dialogue.
    """

    call_count: int = 0

    def chat(self, messages: list[Message]) -> str:
        self.call_count += 1
        last_user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            "",
        )

        # Round 1: model decides it needs the web.
        if self.call_count == 1 and "SEARCH_RESULT" not in last_user:
            # Pull a crude "query" out of the user's question for demo search.
            query = last_user.strip().split("\n")[0][:80] or "python news"
            return f'SEARCH: {query}'

        # Round 2+: model has search results in the conversation — answer.
        return (
            "Based on the search results above, here's a short answer: "
            "this is a mock reply — swap FakeBrain for OllamaBrain to use a real model."
        )


def make_brain(settings: Settings) -> Brain:
    if settings.mock:
        return FakeBrain()
    return OllamaBrain(settings=settings)
