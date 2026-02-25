# Changelog

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
