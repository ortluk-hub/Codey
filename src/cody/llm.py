#"""LLM plumbing for Ollama-backed routing with phase-1 stubs."""

from dataclasses import dataclass
import json
from urllib import request, error


Provider = str


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
    fallback_model: str = "qwen2.5:1.5b

    def route_chat(self, message: str) -> dict:
        # Try primary (cloud) first
        try:
            reply = self.primary_client.chat(message, model=self.primary_model)
            if reply:
                return {"reply": reply, "provider": "qwen3-coder:480b-cloud"}
        except Exception as e:
            print(f"Primary failed: {e}")

        # Try fallback (local)
        try:
            reply = self.fallback_client.chat(message, model=self.fallback_model)
            if reply:
                return {"reply": reply, "provider": "deepseek-coder:6.7b"}
        except Exception as e:
            print(f"Fallback failed: {e}")

        # All failed
        return {
            "reply": f"[stub] Cody received: {message}",
            "provider": "stub",
        }