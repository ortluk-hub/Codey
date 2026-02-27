"""Machine-readable status tracking for Cody phases."""

from pathlib import Path


def _resolve_changelog_path() -> Path:
    """Resolve CHANGELOG.md from the project root, independent of process CWD."""
    status_file = Path(__file__).resolve()
    for parent in status_file.parents:
        candidate = parent / "CHANGELOG.md"
        if candidate.exists():
            return candidate
    return status_file.parents[2] / "CHANGELOG.md"


CHANGELOG_PATH = _resolve_changelog_path()


def _version_headers() -> list[str]:
    """Get all version headers from CHANGELOG.md."""
    if not CHANGELOG_PATH.exists():
        return []
    return [
        line.strip()
        for line in CHANGELOG_PATH.read_text(encoding="utf-8").splitlines()
        if line.startswith("## [")
    ]


def _is_versioned_at_least(version_count: int) -> bool:
    """Check if CHANGELOG.md has at least the specified number of versions."""
    return len(_version_headers()) >= version_count


def get_phase_1_status() -> dict:
    """Get Phase 1 foundation hardening status.

    Returns:
        Dictionary with status checks and completion state.
    """
    status: dict = {
        "tcp_contract_locked": True,
        "docker_policy_validated": True,
        "architecture_metadata_versioned": _is_versioned_at_least(1),
    }
    status["complete"] = all(status.values())
    return status


def get_phase_2_status() -> dict:
    """Get Phase 2 tooling and memory maturity status.

    Returns:
        Dictionary with status checks and completion state.
    """
    status: dict = {
        "tooling_contract_expanded": True,
        "memory_quality_controls": True,
        "phase_2_metadata_versioned": _is_versioned_at_least(2),
    }
    status["complete"] = all(status.values())
    return status


def get_phase_3_status() -> dict:
    """Get Phase 3 delivery and operator visibility status.

    Returns:
        Dictionary with status checks and completion state.
    """
    status: dict = {
        "multi_phase_status_available": True,
        "tcp_contract_supports_phase_3": True,
        "phase_3_metadata_versioned": _is_versioned_at_least(3),
    }
    status["complete"] = all(status.values())
    return status
