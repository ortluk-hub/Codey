"""LLM plumbing for Ollama-backed routing with resilient fallbacks."""

from dataclasses import dataclass, field
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
    pending_messages: list[str] = field(default_factory=list)

    def _compose_message(self, message: str) -> str:
        if not self.pending_messages:
            return message

        queued_messages = "\n".join(f"- {queued}" for queued in self.pending_messages)
        return (
            "System note: these user messages were queued while no LLM provider was available. "
            "Please process them as oldest-to-newest context before answering the latest request.\n\n"
            f"Queued messages:\n{queued_messages}\n\n"
            f"Latest user message:\n{message}"
        )

    def _route_to_provider(self, message: str) -> tuple[str | None, str | None]:
        primary_reply = self.primary_client.chat(message, model=self.primary_model)
        if primary_reply:
            return primary_reply, "ollama-cloud"

        fallback_reply = self.fallback_client.chat(message, model=self.fallback_model)
        if fallback_reply:
            return fallback_reply, "ollama-local"

        return None, None

    def route_chat(self, message: str) -> dict:
        composed_message = self._compose_message(message)
        reply, provider = self._route_to_provider(composed_message)
        if reply and provider:
            self.pending_messages.clear()
            return {"reply": reply, "provider": provider}

        self.pending_messages.append(message)
        return {
            "reply": f"[stub] Cody saved your message while providers are unavailable: {message}",
            "provider": "stub",
            "queued": True,
            "queued_messages": len(self.pending_messages),
        }
