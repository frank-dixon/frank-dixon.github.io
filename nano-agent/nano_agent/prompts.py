"""System prompt + tiny text protocol for tool calls.

Why a text protocol instead of OpenAI-style tool JSON?
  Tiny 1B–3B models are flaky at strict JSON tool schemas.
  A one-line `SEARCH: <query>` convention is dead simple to parse
  and easy to type by hand when you're learning. Upgrade later.

Manual mental model:
  You:   "Who won the Super Bowl in 2026?"
  Model: "SEARCH: Super Bowl 2026 winner"
  You:   (run DuckDuckGo, paste results back as a user message)
  Model: "The winner was ..."
"""

from __future__ import annotations

import re

SYSTEM_PROMPT = """\
You are a tiny local assistant running entirely on the user's machine.

Rules:
1. If you already know the answer from general knowledge, answer directly.
2. If the question needs CURRENT, LOCAL, or SPECIFIC facts you may not have,
   request a web search with EXACTLY one line in this format and nothing else:

   SEARCH: <short search query>

3. After you receive a message starting with SEARCH_RESULT:, use that info
   to answer the user in plain language. Do not invent sources.
4. Keep answers short and clear. No fluff.
"""

# Matches a model reply that is (only) a search request.
_SEARCH_RE = re.compile(
    r"^\s*SEARCH:\s*(.+?)\s*$",
    re.IGNORECASE | re.DOTALL,
)


def parse_search_request(text: str) -> str | None:
    """Return the query if `text` is a SEARCH: line, else None.

    Be slightly forgiving: if the model wraps the line in markdown fences
    or adds a trailing period, still catch it. Tiny models are messy.
    """
    cleaned = text.strip()
    # Strip ``` fences if the model got cute.
    if cleaned.startswith("```") and cleaned.endswith("```"):
        cleaned = cleaned.strip("`").strip()
        if cleaned.lower().startswith("text"):
            cleaned = cleaned[4:].strip()

    match = _SEARCH_RE.match(cleaned)
    if match:
        return match.group(1).strip().strip('"').strip("'")

    # Fallback: SEARCH: appears on its own line somewhere in the reply.
    for line in cleaned.splitlines():
        match = _SEARCH_RE.match(line)
        if match:
            return match.group(1).strip().strip('"').strip("'")
    return None


def format_search_result_message(query: str, results_text: str) -> str:
    """Stuff tool output back into the chat as a user message.

    Tiny models often lack a dedicated `tool` role. Treating the result as
    another user message is the pragmatic move — and it's what you'd do
    manually in a chat UI anyway.
    """
    return (
        f"SEARCH_RESULT: query={query!r}\n"
        f"{results_text.strip()}\n\n"
        "Using only the result above, answer the original question."
    )
