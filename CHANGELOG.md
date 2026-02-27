# Changelog

## [0.2.0] - 2026-02-26

### Added
- Implemented **tool execution** with `ToolExecutor` class that runs Python code in the Docker sandbox for direct computation results.
- Added **intent-based routing** that detects simple math expressions (e.g., "What is 2 + 2 * 10?") and executes them locally without using cloud LLM credits.
- Added `extract_code_block()` utility function to parse Python code from markdown responses.
- Added `/run` POST endpoint to FastAPI for direct sandbox code execution.
- Added comprehensive unit tests for tool execution, intent routing, and sandbox functionality.

### Changed
- Increased sandbox timeout from 5s to 30s for complex code execution.
- Increased Ollama client timeout from 5s to 30s for larger model responses.
- Updated intent resolution to use regex pattern matching for reliable math detection instead of relying on tiny LLM classification.

### Fixed
- Fixed `sandbox` import in `api_ui.py` to support the new `/run` endpoint.
- Fixed uvicorn run command to use full module path `cody.api_ui:app`.

## [0.1.10] - 2026-02-26

### Added
- Added environment variable support for Ollama URLs (`CODY_OLLAMA_PRIMARY_URL`, `CODY_OLLAMA_FALLBACK_URL`, `CODY_OLLAMA_INTENT_URL`) to allow configuration without code changes.
- Added `CONTRIBUTING.md` with development setup instructions, code quality guidelines, and contribution workflow.
- Added `pyproject.toml` for proper package installation with `pip install -e ".[dev]"`.
- Added `__init__.py` to tests directory for reliable test discovery.
- Added type hints and docstrings to `sandbox.py` and `status.py`.

### Changed
- Changed default Ollama URL from hardcoded IP to `http://127.0.0.1:11434` (configurable via environment).
- Updated `requirements.txt` to include development dependencies (pytest, mypy, ruff).
- Consolidated changelog versioning logic between `cody/status.py` and `codey/project.py`.

### Fixed
- Fixed package imports throughout `src/cody/` to use consistent `from . import ...` pattern.
- Fixed test imports to use `from cody.*` package-style imports.

## [0.1.9] - 2026-02-26

### Added
- Added structured logging configuration to `api_ui.py` for visibility into LLM routing decisions.
- Added test script `test_cody.sh` for comprehensive integration testing of routing behavior.

### Changed
- Updated LLM routing flow: Intent Resolver → (Tool Execution OR Cloud/Local Fallback) → Stub.

## [0.1.8] - 2026-02-26

### Added
- Added fallback chain verification tests showing Cloud → Local → Stub progression.
- Added network isolation and read-only filesystem verification for sandbox security.

## [0.1.7] - 2026-02-26
- Added a first-time environment setup section to `README.md` with virtualenv creation, dependency installation, and `PYTHONPATH=src/cody:src` guidance so users can run/test successfully on initial setup.

## [0.1.6] - 2026-02-26
- Added structured LLM lifecycle logging in `LLMRouter` with `request_id`, selected model/provider, and response recipient metadata.
- Extended TCP and API chat flows to propagate request tracing metadata into router calls for end-to-end request visibility.
- Added unit tests for LLM lifecycle log events and router metadata forwarding in chat command handling.

## [0.1.5] - 2026-02-26
- Added resilient stub recovery in `LLMRouter` to queue user messages while providers are unavailable and replay queued context to the first recovered provider call.
- Switched API and TCP chat handlers to use a shared router instance so queued stub messages persist across requests.
- Added unit tests covering message queueing during stub mode and queued-message replay on provider recovery.

## [1.3.1] - 2026-02-26

### Fixed
- Fixed package import paths in `src/cody` modules to use package-relative imports so test and runtime imports resolve reliably.
- Repaired a syntax error in `src/cody/llm.py` and hardened routing fallback behavior to return stable provider badges.
- Corrected the primary Ollama endpoint port in config from `1134` to `11434`.

## [1.3.0] - 2026-02-26

### Added
- Added a lightweight web chat interface at `GET /` in the FastAPI app so users can send messages to Cody from a browser.
- Added `render_chat_page()` helper to keep the chat page HTML generation testable and isolated from routing.
- Added unit tests validating that the chat page includes the form, title, and `POST /chat` integration.

## [1.2.0] - 2026-02-25

### Added
- Implemented Cody Phase 3 status tracking with `get_phase_3_status` and completion gate checks for multi-phase readiness, TCP support, and changelog versioning depth.
- Added TCP command `get_phase_3_status` so NDJSON clients can query Phase 3 readiness.
- Expanded FastAPI `/status` response to include phase-3 status alongside existing phase checks.
- Added unit tests for Phase 3 status payload shape and Phase 3 TCP command behavior.

## [1.1.0] - 2026-02-25

### Added
- Implemented Cody Phase 2 status tracking with `get_phase_2_status` and completion gate checks for tooling, memory controls, and changelog versioning.
- Added TCP command `get_phase_2_status` so NDJSON clients can query Phase 2 readiness.
- Expanded FastAPI `/status` response to include both phase-1 and phase-2 status payloads.
- Added memory summary validation so long-term summaries require non-empty `topic` and `summary` fields.
- Added unit tests for Phase 2 status shape, Phase 2 TCP command behavior, and memory summary validation.

## [1.0.0] - 2026-02-25

### Added
- Implemented Phase 1 Cody package under `src/cody` with modular components for TCP server, FastAPI UI, sandbox, LLM routing, memory, config, and status.
- Added NDJSON TCP contract on port 8888 with safe framing validation and command handlers for `ping`, `run`, `chat`, and `get_phase_1_status`.
- Added Docker sandbox policy object with restriction flag generation and subprocess-based runner that handles missing Docker clearly.
- Added FastAPI endpoints `/health`, `/chat`, and `/status` with provider badge plumbing.
- Added short-term in-memory and long-term JSON memory persistence implementation.
- Added unit tests for TCP protocol framing, Docker policy flags, memory storage, and status shape.
- Added `requirements.txt` and updated README with run/test instructions.
