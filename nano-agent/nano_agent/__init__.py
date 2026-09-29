"""nano_agent — a tiny local LLM + optional web search, built to be readable.

Trace the code in this order when learning by hand:

  1. llm.py          — how we talk to a model on your machine
  2. tools/web_search.py — how we look things up
  3. prompts.py      — how we teach the model WHEN to search
  4. agent.py        — the think → (maybe tool) → answer loop
  5. __main__.py     — the CLI you actually run

No LangChain. No magic. Just HTTP + a while-loop + JSON.
"""

__version__ = "0.1.0"
