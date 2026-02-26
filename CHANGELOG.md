# Changelog

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
