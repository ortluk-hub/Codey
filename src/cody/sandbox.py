"""Docker sandbox runner for executing Python code with strict restrictions."""

from dataclasses import dataclass
import subprocess


@dataclass(frozen=True)
class DockerPolicy:
    """Policy configuration for Docker sandbox execution."""

    image: str = "python:3.12-alpine"
    timeout_seconds: int = 5
    memory: str = "128m"
    cpus: str = "0.5"
    pids_limit: int = 64
    user: str = "65534:65534"
    network_none: bool = True
    read_only: bool = True
    cap_drop_all: bool = True

    def to_docker_flags(self) -> list[str]:
        """Generate Docker CLI flags from policy settings."""
        flags: list[str] = [
            "--rm",
            "--memory",
            self.memory,
            "--cpus",
            self.cpus,
            "--pids-limit",
            str(self.pids_limit),
            "--user",
            self.user,
            "--workdir",
            "/sandbox",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,size=16m",
            "--tmpfs",
            "/sandbox:rw,noexec,nosuid,size=16m",
        ]
        if self.network_none:
            flags.extend(["--network", "none"])
        if self.read_only:
            flags.append("--read-only")
        if self.cap_drop_all:
            flags.extend(["--cap-drop", "ALL"])
        return flags


def run_python_in_docker(code: str, policy: DockerPolicy | None = None) -> dict:
    """Execute Python code in a Docker sandbox with the given policy.

    Args:
        code: Python code to execute.
        policy: Optional DockerPolicy configuration. Uses defaults if not provided.

    Returns:
        Dictionary with execution result containing 'ok', 'stdout', 'stderr', 'exit_code',
        or 'error' and 'message' on failure.
    """
    sandbox_policy = policy or DockerPolicy()
    cmd: list[str] = [
        "docker",
        "run",
        *sandbox_policy.to_docker_flags(),
        sandbox_policy.image,
        "python",
        "-c",
        code,
    ]
    try:
        completed = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            timeout=sandbox_policy.timeout_seconds,
        )
    except FileNotFoundError:
        return {
            "ok": False,
            "error": "docker_not_available",
            "message": "Docker executable not found. Install Docker to use run command.",
        }
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "error": "sandbox_timeout",
            "message": "Sandbox execution exceeded timeout.",
        }

    return {
        "ok": True,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "exit_code": completed.returncode,
    }
