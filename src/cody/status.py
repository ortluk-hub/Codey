"""Phase-1 machine-readable status tracking."""

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


def _has_version_header() -> bool:
    if not CHANGELOG_PATH.exists():
        return False
    for line in CHANGELOG_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("## ["):
            return True
    return False


def get_phase_1_status() -> dict:
    status = {
        "tcp_contract_locked": True,
        "docker_policy_validated": True,
        "architecture_metadata_versioned": _has_version_header(),
    }
    status["complete"] = all(status.values())
    return status
