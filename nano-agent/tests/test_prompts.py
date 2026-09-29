"""Unit tests you can run without Ollama, DuckDuckGo, or API keys."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nano_agent.prompts import format_search_result_message, parse_search_request


def test_parse_plain_search() -> None:
    assert parse_search_request("SEARCH: python 3.13") == "python 3.13"


def test_parse_search_is_case_insensitive() -> None:
    assert parse_search_request("search: hello world") == "hello world"


def test_parse_ignores_normal_answers() -> None:
    assert parse_search_request("Paris is the capital of France.") is None


def test_parse_search_inside_multiline() -> None:
    text = "Sure.\nSEARCH: oscars 2026 winners\n"
    assert parse_search_request(text) == "oscars 2026 winners"


def test_format_search_result_message() -> None:
    msg = format_search_result_message("cats", "1. Cat page\n   meow")
    assert msg.startswith("SEARCH_RESULT:")
    assert "cats" in msg
    assert "meow" in msg
