"""Configuration values for Cody."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    tcp_host: str = "0.0.0.0"
    tcp_port: int = 8888
    long_term_memory_path: str = "data/long_term_memory.json"

    # All point to local Ollama server
    ollama_intent_url: str = "http://100.108.217.7:11434"
    ollama_primary_url: str = "http://100.108.217.7:1134"
    ollama_fallback_url: str = "http://100.108.217.7:11434"    
    # Models (from your ollama list)
    intent_model: str = "qwen3:0.6b"           # Fast, small
    primary_model: str = "qwen3-coder:480b-cloud"  # Cloud, powerful
    fallback_model: str = "deepseek-coder:6.7b"    # Local backup

DEFAULT_SETTINGS = Settings()
