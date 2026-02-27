# Contributing to Codey

Thank you for your interest in contributing to Codey! This document provides guidelines and setup instructions for developers.

## Development Setup

### Prerequisites

- Python 3.12 or higher
- pip or uv for package management
- Docker (optional, for sandbox testing)
- Ollama server (optional, for LLM integration testing)

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Codey
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Set PYTHONPATH** (if not using editable install)
   ```bash
   # On Windows
   set PYTHONPATH=src
   # On macOS/Linux
   export PYTHONPATH=src
   ```

### Environment Variables

Configure optional environment variables for custom behavior:

| Variable | Description | Default |
|----------|-------------|---------|
| `CODY_OLLAMA_INTENT_URL` | URL for intent resolver Ollama server | `http://127.0.0.1:11434` |
| `CODY_OLLAMA_PRIMARY_URL` | URL for primary Ollama server | `http://127.0.0.1:11434` |
| `CODY_OLLAMA_FALLBACK_URL` | URL for fallback Ollama server | `http://127.0.0.1:11434` |

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Or using unittest
python -m unittest discover -s tests -v
```

## Code Quality

This project uses the following tools for code quality:

- **ruff** - Linting and formatting
- **mypy** - Type checking

```bash
# Run linter
ruff check src/ tests/

# Run type checker
mypy src/ tests/

# Format code
ruff format src/ tests/
```

## Project Structure

```
Codey/
├── src/
│   ├── cody/          # Runtime implementation
│   │   ├── __init__.py
│   │   ├── api_ui.py  # FastAPI web endpoints
│   │   ├── config.py  # Configuration
│   │   ├── llm.py     # LLM routing
│   │   ├── memory.py  # Memory storage
│   │   ├── sandbox.py # Docker sandbox
│   │   ├── status.py  # Phase status
│   │   └── tcp_server.py  # TCP server
│   └── codey/         # Architecture metadata
│       ├── __init__.py
│       └── project.py # Architecture definitions
├── tests/
│   ├── test_api_ui.py
│   ├── test_docker_policy.py
│   ├── test_llm.py
│   ├── test_memory.py
│   ├── test_project.py
│   ├── test_status.py
│   └── test_tcp_protocol.py
├── CHANGELOG.md
├── CONTRIBUTING.md
├── README.md
├── pyproject.toml
└── requirements.txt
```

## Running the Services

### TCP Server
```bash
python -m cody.tcp_server
# Or: cody-tcp
```

### API UI (FastAPI)
```bash
python -m cody.api_ui
# Or: cody-api
```

## Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the existing code style

3. **Add tests** for new functionality

4. **Run tests and linting** to ensure everything passes

5. **Update CHANGELOG.md** with your changes

6. **Commit and push**
   ```bash
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**

## Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Be concise but descriptive
- Reference issues when applicable

## Questions?

Feel free to open an issue for any questions or discussions about contributing.
