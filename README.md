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

## Roadmap

### Phase 1: Foundation hardening
- Lock communication contract for TCP port `8888` and FastAPI chat UI.
- Validate Docker sandbox runtime policies through automated unit checks.
- Keep modular architecture metadata versioned through changelog updates.
- Track phase completion via `get_phase_1_status()` for an explicit machine-readable result.

### Phase 2: Tooling and memory maturity
- Broaden tool contract to support richer coding workflows.
- Refine summarized long-term memory strategy quality controls.
- Add test coverage around architecture regressions and memory expectations.

### Phase 3: Delivery and operator visibility
- Expose roadmap-aligned status reporting in project documentation.
- Define release readiness criteria for model fallback behavior.
- Document production runbooks for Cody service operators.

## Development

Run tests with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'
```
