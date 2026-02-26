"""LLM plumbing for Ollama-backed routing with resilient fallbacks."""

from dataclasses import dataclass
import json
from urllib import error, request


@dataclass
class OllamaClient:
    endpoint: str | None

    def chat(self, message: str, model: str) -> str | None:
        if not self.endpoint:
            return None

        payload = json.dumps({"model": model, "prompt": message, "stream": False}).encode()
        req = request.Request(
            self.endpoint.rstrip("/") + "/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=5) as resp:
                raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            return data.get("response")
        except (error.URLError, TimeoutError, json.JSONDecodeError):
            return None


@dataclass
class LLMRouter:
    intent_client: OllamaClient
    primary_client: OllamaClient
    fallback_client: OllamaClient

    intent_model: str = "qwen3:0.6b"
    primary_model: str = "qwen3-coder:480b-cloud"
    fallback_model: str = "deepseek-coder:6.7b"

    @staticmethod
    def _safe_chat(client: OllamaClient, message: str, model: str) -> str | None:
        try:
            return client.chat(message, model=model)
        except Exception:
            return None

    def route_chat(self, message: str) -> dict:
        reply = self._safe_chat(self.primary_client, message, model=self.primary_model)
        if reply:
            return {"reply": reply, "provider": "ollama-cloud"}

        reply = self._safe_chat(self.fallback_client, message, model=self.fallback_model)
        if reply:
            return {"reply": reply, "provider": "ollama-local"}

        return {"reply": f"[stub] Cody received: {message}", "provider": "stub"}
