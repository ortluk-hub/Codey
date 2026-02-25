# Changelog

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
