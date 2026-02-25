# Changelog

## [0.5.0] - 2026-02-25

### Added
- Added `PhaseStatus` and `get_phase_1_status()` to provide a machine-readable completion signal for Phase 1 goals.
- Added unit tests validating that Phase 1 reports complete with three passing checks.
- Documented Phase 1 status tracking in the roadmap section of README.

## [0.4.0] - 2026-02-25

### Added
- Added a formal three-phase roadmap contract with milestones and outcomes exposed from `codey.project`.
- Added roadmap unit tests to ensure milestone structure and outcome quality remain stable.
- Documented roadmap phases in README for quick operator visibility.

## [0.3.0] - 2026-02-25

### Changed
- Updated the Cody architecture contract to represent the coder-agent framework with TCP communication and web UI integration.
- Added a communication configuration object covering TCP port `8888` and FastAPI chat UI provider badges.
- Updated the LLM stack contract to use `ollama-cloud` primary, `ollama-local-tiny` intent resolver, and `ollama-local` fallback.
- Extended runtime policy with explicit Docker execution environment metadata.
- Refreshed README and tests to validate the new framework contract end-to-end.

## [0.2.0] - 2026-02-25

### Changed
- Replaced generic identity scaffold with a concrete architecture contract for Cody as a modular coding agent.
- Defined model stack with `qwen3-coder:480b-cloud` as primary and `qwen2.5:1.5b` as local fallback, both Ollama-served.
- Added explicit runtime policy for containerized sandbox execution and context-scoped command usage.
- Added memory strategy fields for short-term full context and long-term summarized memory.
- Expanded unit coverage to validate architecture, model selection, runtime policy, and memory policy.

## [0.1.0] - 2026-02-25

### Added
- Established Codey project identity as a standalone project.
- Explicitly marked Codey as not being an Orty bot type.
- Added unit tests to validate the project identity contract.
