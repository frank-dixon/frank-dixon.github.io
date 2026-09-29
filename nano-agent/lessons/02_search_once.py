#!/usr/bin/env python3
"""Lesson 02 — search the web ONCE. No LLM.

Goal: see what DuckDuckGo returns so you know what the model will read.

  cd nano-agent
  pip install -r requirements.txt
  python lessons/02_search_once.py "python 3.13 release notes"
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nano_agent.tools.web_search import search_web


def main() -> None:
    query = " ".join(sys.argv[1:]) or "local LLM on MacBook"
    print(f"query={query!r}\n---")
    print(search_web(query, max_results=5))


if __name__ == "__main__":
    main()
