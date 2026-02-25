"""Phase-1 machine-readable status tracking."""

from pathlib import Path


CHANGELOG_PATH = Path("CHANGELOG.md")


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
