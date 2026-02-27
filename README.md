# Codey/Cody - Modular Coding Assistant Framework

**Codey** (also known as Cody) is a modular coding assistant framework with intelligent routing, sandboxed code execution, and multi-tier LLM fallback support.

## Features

- **Intent-Based Routing**: Simple math expressions are executed locally using Python sandbox, saving cloud LLM credits
- **Tool Execution**: Direct code execution in a secure Docker sandbox with network isolation and read-only filesystem
- **LLM Fallback Chain**: Cloud → Local → Stub, ensuring availability even when providers are down
- **Multiple Interfaces**: Web UI (FastAPI) and TCP server (NDJSON protocol)
- **Phase Tracking**: Built-in status gates for Phase 1/2/3 completion criteria

## Architecture

```
User Request → Intent Resolver → Tool Execution (for math)
                              → Cloud LLM (for reasoning)
                                   ↓
                              Local Fallback
                                   ↓
                              Stub (queue for replay)
```

## Modules

`src/cody/` contains:
- `tcp_server.py` - NDJSON TCP server on port 8888
- `api_ui.py` - FastAPI web UI with chat and sandbox endpoints
- `sandbox.py` - Docker sandbox runner with security policies
- `llm.py` - Ollama client with intent routing and tool execution
- `memory.py` - Short-term and long-term memory storage
- `config.py` - Runtime settings with environment variable support
- `status.py` - Phase 1/2/3 status gates

`src/codey/` contains:
- `project.py` - Architecture definitions and roadmap metadata

## Environment Setup

### First-Time Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or install as editable package
pip install -e ".[dev]"
```

### Configure Ollama URLs (Optional)

By default, Codey connects to `http://127.0.0.1:11434`. To use a different Ollama server:

```bash
export CODY_OLLAMA_PRIMARY_URL=http://your-ollama-host:11434
export CODY_OLLAMA_FALLBACK_URL=http://your-ollama-host:11434
export CODY_OLLAMA_INTENT_URL=http://your-ollama-host:11434
```

### Set PYTHONPATH

```bash
export PYTHONPATH=src
```

For persistence, add to `~/.bashrc`.

## Running Codey

### Web UI (FastAPI)

```bash
python -m cody.api_ui
```

Access at `http://localhost:8000/`:
- `/` - Chat UI
- `/health` - Health check
- `/status` - Phase status
- `/run` (POST) - Execute code in sandbox

### TCP Server

```bash
python -m cody.tcp_server
```

Connect via netcat or any TCP client to `localhost:8888`.

## API Endpoints

### Web API

| Method | Endpoint | Request | Response |
|--------|----------|---------|----------|
| GET | `/health` | - | `{"status":"ok","service":"cody"}` |
| GET | `/` | - | Chat UI HTML |
| GET | `/status` | - | Phase 1/2/3 status |
| POST | `/chat` | `{"message":"..."}` | `{"reply":"...","provider":"..."}` |
| POST | `/run` | `{"code":"print(1)"}` | `{"ok":true,"stdout":"1\n",...}` |

### TCP Protocol (NDJSON)

Send one JSON object per line:

```json
{"cmd":"ping"}
{"cmd":"run","language":"python","code":"print(1)"}
{"cmd":"chat","message":"What is 2 + 2?"}
{"cmd":"get_phase_1_status"}
{"cmd":"get_phase_2_status"}
{"cmd":"get_phase_3_status"}
```

Responses:
```json
{"ok":true,"reply":"pong"}
{"ok":true,"reply":"Result: 4","provider":"local-tool"}
{"ok":true,"reply":"...","provider":"ollama-cloud"}
```

## Provider Badge Values

- `local-tool` - Executed directly in sandbox (no LLM)
- `ollama-cloud` - Primary cloud LLM
- `ollama-local` - Local fallback LLM
- `stub` - All providers unavailable, message queued

## Testing

### Run All Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

### Integration Test Script

```bash
./test_cody.sh
```

### Test Coverage

Tests cover:
- TCP protocol framing and commands
- Docker sandbox policy and execution
- LLM routing and fallback behavior
- Intent detection and tool execution
- Memory storage and retrieval
- Phase status gates
- API UI endpoints

## Security

The Docker sandbox enforces:
- **No network access** (`--network none`)
- **Read-only filesystem** (`--read-only`)
- **Dropped capabilities** (`--cap-drop ALL`)
- **Resource limits** (CPU, memory, PIDs)
- **Non-root user** (`--user 65534:65534`)

## Requirements

- Python 3.12+
- Docker (for sandbox execution)
- Ollama server (for LLM responses)
- FastAPI + uvicorn (for web UI)

## License

MIT
