# Codey

Codey defines the architecture contract for **Cody**, a modular coding agent.

## Agent architecture

Cody is specified as:
- modular by design
- powered by a very small LLM for intent resolution and tool calling
- equipped with full tool and filesystem command access within a **containerized sandbox**
- constrained by system-prompt-assigned execution context
- memory-managed with short-term full context and long-term summarized memory

## LLM stack

All models are Ollama-served:
- Primary: `qwen3-coder:480b-cloud`
- Local fallback: `qwen2.5:1.5b`

## Development

Run tests with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'
```
