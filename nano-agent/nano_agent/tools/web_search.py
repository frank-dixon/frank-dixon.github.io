"""Web search via DuckDuckGo — no API key, no account.

Manual equivalent:
  - Open duckduckgo.com, type a query, skim the top links.
  - Or: `curl` somehow... but DDG HTML is annoying, so we use the `ddgs` package.

Privacy note: the SEARCH leaves your machine (that's the point of "search the web").
The LLM itself still runs 100% local. Only the query + result snippets travel.
"""

from __future__ import annotations

from typing import Any


def search_web(query: str, max_results: int = 5) -> str:
    """Run a DuckDuckGo text search and return a plain-text digest for the LLM.

    Returns a numbered list the model can quote from. If search fails
    (network, package missing, rate limit), returns an error string instead
    of raising — the agent loop can still finish with a graceful apology.
    """
    query = (query or "").strip()
    if not query:
        return "ERROR: empty search query."

    try:
        # Import inside the function so `NANO_MOCK=1` lessons don't require ddgs
        # until you actually search. Also keeps import errors readable.
        from ddgs import DDGS
    except ImportError:
        return (
            "ERROR: package `ddgs` is not installed. "
            "Run: pip install -r requirements.txt"
        )

    try:
        # DDGS().text returns an iterator/list of dicts with title/href/body.
        raw: list[dict[str, Any]] = list(
            DDGS().text(query, max_results=max_results)
        )
    except Exception as exc:  # noqa: BLE001 — surface any network weirdness
        return f"ERROR: search failed ({type(exc).__name__}: {exc})"

    if not raw:
        return "No results found."

    lines: list[str] = []
    for i, hit in enumerate(raw, start=1):
        title = (hit.get("title") or "").strip()
        href = (hit.get("href") or hit.get("link") or "").strip()
        body = (hit.get("body") or hit.get("snippet") or "").strip()
        lines.append(f"{i}. {title}\n   URL: {href}\n   {body}")
    return "\n".join(lines)
