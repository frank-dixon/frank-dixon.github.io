# Nano Agent — local micro LLM + optional web search (+ later: voice)

A **CLI-only** learning project. No GUI. You run everything in the terminal so you can see each step.

Goal: a tiny assistant that:

1. Runs a **local** LLM on your MacBook (via [Ollama](https://ollama.com))
2. **Searches the web** when it needs fresher facts (DuckDuckGo, no API key)
3. Optionally **speaks** the answer later (macOS `say`, or studio-quality ElevenLabs / Grok TTS)

The code is intentionally small and heavily commented so you can trace it and recreate the pattern yourself.

---

## What’s out there (short map)

| Approach | Best for | Notes |
|----------|----------|--------|
| **Ollama** + tiny models | Learning + daily Mac use | Easiest install. `llama3.2:1b`, `gemma2:2b`, `phi3:mini` |
| **MLX / mlx-lm** | Max speed on Apple Silicon | Native Metal; steeper than Ollama |
| **llama.cpp** | GGUF everywhere | Great control; more manual |
| **mlx-code**, **agent-framework-mlx** | Full Mac agents | Powerful; harder to “see the loop” |
| **TinyLLM** | Chat UI + local backends | More product than textbook |

This repo picks **Ollama + a plain Python agent loop** so nothing is hidden behind a framework.

---

## Trace path (learn by reading)

Read in this order:

| Step | File | What you learn |
|------|------|----------------|
| 1 | `nano_agent/llm.py` | One chat HTTP call to Ollama |
| 2 | `nano_agent/tools/web_search.py` | One DuckDuckGo search |
| 3 | `nano_agent/prompts.py` | When to search (`SEARCH: …`) |
| 4 | `nano_agent/agent.py` | The think → tool → answer loop |
| 5 | `nano_agent/__main__.py` | CLI wiring |
| 6 *(later)* | `nano_agent/voice/` | Bolt on TTS without a GUI |

Lessons you can run:

```bash
cd nano-agent
pip install -r requirements.txt

# Offline: no model needed
NANO_MOCK=1 python lessons/01_chat_once.py
python lessons/02_search_once.py "local LLM MacBook"
NANO_MOCK=1 python lessons/03_agent_loop.py "what's new in python?"

# Later module — voice (practice with macOS say, or cloud TTS)
NANO_MOCK=1 NANO_VOICE=file python lessons/04_voice_speak.py "say hello"
```

---

## MacBook setup (real local brain)

```bash
# 1) Install Ollama from https://ollama.com , then:
ollama pull llama3.2:1b          # nano (~1.3 GB) — great for learning
# ollama pull llama3.2           # micro 3B — nicer answers, still light

cd nano-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m nano_agent "What is 2+2?"
python -m nano_agent "Who won the Super Bowl most recently?"
```

Suggested models by RAM:

- **8 GB:** `llama3.2:1b`, `gemma2:2b`
- **16 GB:** `llama3.2` (3B), `phi3:mini`
- **16 GB+ headroom:** `gemma2:9b`, larger MLX models if you graduate off Ollama

---

## CLI reference (no GUI)

```bash
# Text only
python -m nano_agent "Your question"

# Hide the think/search trace
python -m nano_agent --quiet "Your question"

# Practice the loop without Ollama
python -m nano_agent --mock "latest python news"

# Optional voice (still terminal — plays via afplay/say or writes a file)
python -m nano_agent --speak --voice say "Tell me a one-line joke"
python -m nano_agent --speak --voice file "Write this to a stub file"

# Studio-quality cloud TTS (API keys required; LLM can stay local)
export ELEVENLABS_API_KEY=...
pip install elevenlabs
python -m nano_agent --speak --voice elevenlabs "Hello from ElevenLabs"

export XAI_API_KEY=...
python -m nano_agent --speak --voice grok "Hello from Grok voice"
```

Pipe a question:

```bash
echo "capital of Japan" | python -m nano_agent
```

---

## Later learning module: voice

Voice is **intentionally separate**. Get the text agent solid first, then add speech.

| Backend | Quality | Needs | Flag |
|---------|---------|-------|------|
| `say` | Robotic (fine for learning) | macOS only | `--voice say` |
| `file` | Silent stub | Nothing | `--voice file` |
| `elevenlabs` | Excellent | `ELEVENLABS_API_KEY` + `pip install elevenlabs` | `--voice elevenlabs` |
| `grok` | Excellent | `XAI_API_KEY` | `--voice grok` |

Important tradeoff: the **LLM stays local**; the nicest voices send text to ElevenLabs or xAI and get audio back. Fully local voices exist (`say`, Piper, mlx-audio) but will not match those APIs.

See `lessons/04_voice_speak.py` and `nano_agent/voice/`.

---

## Env knobs

| Variable | Default | Meaning |
|----------|---------|---------|
| `NANO_MODEL` | `llama3.2:1b` | Ollama model name |
| `NANO_OLLAMA_HOST` | `http://127.0.0.1:11434` | Ollama base URL |
| `NANO_MOCK` | off | Use scripted FakeBrain |
| `NANO_MAX_TOOL_ROUNDS` | `3` | Search loop cap |
| `NANO_VOICE` | `say` on Mac, else `file` | Default TTS backend |
| `ELEVENLABS_API_KEY` | — | ElevenLabs |
| `ELEVENLABS_VOICE_ID` | docs demo voice | Optional override |
| `XAI_API_KEY` | — | Grok / xAI TTS |
| `XAI_VOICE_ID` | `eve` | Grok voice |

---

## Tests

```bash
cd nano-agent
pip install -r requirements.txt pytest
NANO_MOCK=1 python -m pytest -q
```

---

## Privacy in one line

Chat with the model stays on your machine (Ollama). A `SEARCH:` round trips through DuckDuckGo. Cloud TTS sends the **final answer text** to ElevenLabs or xAI.
