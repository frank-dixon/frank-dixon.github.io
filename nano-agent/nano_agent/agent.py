"""The agent loop — this is the whole trick.

Pseudocode you'd write on a napkin:

    messages = [system, user_question]
    for _ in range(max_rounds):
        reply = brain.chat(messages)
        if reply starts with SEARCH:
            results = duckduckgo(query)
            messages.append(assistant_reply)
            messages.append(search_results_as_user_msg)
            continue
        return reply   # final answer

That's it. Frameworks just hide this loop behind 14 abstractions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .config import Settings
from .llm import Brain, Message, make_brain
from .prompts import (
    SYSTEM_PROMPT,
    format_search_result_message,
    parse_search_request,
)
from .tools import search_web


# Optional hook so the CLI (or tests) can print each step as it happens.
Tracer = Callable[[str], None]


def _noop(_msg: str) -> None:
    pass


@dataclass
class Agent:
    settings: Settings
    brain: Brain = field(init=False)
    trace: Tracer = field(default=_noop)

    def __post_init__(self) -> None:
        self.brain = make_brain(self.settings)

    def ask(self, question: str) -> str:
        question = question.strip()
        if not question:
            return "Ask me something, dude."

        messages: list[Message] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ]
        self.trace(f"user: {question}")

        for round_i in range(1, self.settings.max_tool_rounds + 1):
            self.trace(f"── brain round {round_i} ──")
            reply = self.brain.chat(messages)
            self.trace(f"assistant: {reply}")

            query = parse_search_request(reply)
            if query is None:
                # Model answered directly. Done.
                return reply

            # Model wants the web. Run the tool, feed results back, loop.
            self.trace(f"tool web_search: {query!r}")
            results = search_web(query, max_results=self.settings.search_max_results)
            self.trace(f"tool result:\n{results}")

            messages.append({"role": "assistant", "content": reply})
            messages.append(
                {
                    "role": "user",
                    "content": format_search_result_message(query, results),
                }
            )

        return (
            "I kept wanting to search and hit the round limit. "
            "Try a clearer question, or bump NANO_MAX_TOOL_ROUNDS."
        )


def run_once(question: str, settings: Settings | None = None, trace: Tracer = _noop) -> str:
    """Convenience for scripts and lessons."""
    agent = Agent(settings=settings or Settings(), trace=trace)
    return agent.ask(question)
