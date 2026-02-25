# Codey

Codey defines the architecture contract for **Cody**, a modular coder agent framework.

## Agent architecture

Cody is specified as:
- modular by design
- reachable via TCP server commands on port `8888`
- equipped with tool support and filesystem command access
- sandboxed through Docker for safe code execution
- surfaced through a FastAPI web UI chat with provider badges
- memory-managed with short-term full context and long-term summarized memory

## LLM stack

All models are Ollama-served:
- Primary: `ollama-cloud`
- Intent resolver: `ollama-local-tiny`
- Local fallback: `ollama-local`

## Development

Run tests with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'
```
