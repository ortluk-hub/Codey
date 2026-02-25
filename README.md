# Cody Phase 1 Foundation

Cody is a modular coding assistant foundation implemented in Python 3.12, now with Phase 3 status orchestration and maturity checks.

## Modules

`src/cody/` contains:
- `tcp_server.py` NDJSON TCP contract on port 8888
- `api_ui.py` FastAPI web UI endpoints
- `sandbox.py` Docker sandbox runner + policy object
- `llm.py` Ollama client + routing plumbing
- `memory.py` short-term and long-term memory storage
- `config.py` runtime settings
- `status.py` Phase 1/2/3 status gates

## Entrypoints

```bash
python -m cody.tcp_server
python -m cody.api_ui
```

## TCP Protocol (NDJSON)

One JSON object per line.

- `{"cmd":"ping"}`
- `{"cmd":"run","language":"python","code":"print(1)"}`
- `{"cmd":"chat","message":"hello"}`
- `{"cmd":"get_phase_1_status"}`
- `{"cmd":"get_phase_2_status"}`
- `{"cmd":"get_phase_3_status"}`

## API Endpoints

- `GET /health` -> `{"status":"ok","service":"cody"}`
- `POST /chat` with `{"message":"..."}` -> `{"reply":"...","provider":"..."}`
- `GET /status` -> object containing phase-1, phase-2, and phase-3 status checks

Provider badge values are wired as:
- `ollama-cloud`
- `ollama-local-tiny`
- `ollama-local`
- `stub`

## Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'
```
