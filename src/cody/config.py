"""Configuration values for Cody."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    tcp_host: str = "0.0.0.0"
    tcp_port: int = 8888
    long_term_memory_path: str = "data/long_term_memory.json"
    ollama_primary_url: str | None = None
    ollama_intent_url: str | None = None
    ollama_fallback_url: str | None = None


DEFAULT_SETTINGS = Settings()
