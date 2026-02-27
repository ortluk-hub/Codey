"""Configuration values for Cody."""

from dataclasses import dataclass
import os


def _get_env_url(key: str, default: str) -> str:
    """Get Ollama URL from environment or use default."""
    return os.environ.get(key, default)


@dataclass(frozen=True)
class Settings:
    tcp_host: str = "0.0.0.0"
    tcp_port: int = 8888
    long_term_memory_path: str = "data/long_term_memory.json"

    # All point to local Ollama server (configurable via environment variables)
    ollama_intent_url: str = None  # type: ignore
    ollama_primary_url: str = None  # type: ignore
    ollama_fallback_url: str = None  # type: ignore
    # Models (from your ollama list)
    intent_model: str = "qwen3:0.6b"           # Fast, small
    primary_model: str = "qwen3-coder:480b-cloud"  # Cloud, powerful
    fallback_model: str = "deepseek-coder:6.7b"    # Local backup


DEFAULT_SETTINGS = Settings(
    ollama_intent_url=_get_env_url("CODY_OLLAMA_INTENT_URL", "http://127.0.0.1:11434"),
    ollama_primary_url=_get_env_url("CODY_OLLAMA_PRIMARY_URL", "http://127.0.0.1:11434"),
    ollama_fallback_url=_get_env_url("CODY_OLLAMA_FALLBACK_URL", "http://127.0.0.1:11434"),
)
