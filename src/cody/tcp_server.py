"""NDJSON TCP server for Cody."""

import json
import socketserver

from cody.config import DEFAULT_SETTINGS
from cody.llm import LLMRouter, OllamaClient
from cody.sandbox import run_python_in_docker
from cody.status import get_phase_1_status


def _build_router() -> LLMRouter:
    return LLMRouter(
        intent_client=OllamaClient(DEFAULT_SETTINGS.ollama_intent_url),
        primary_client=OllamaClient(DEFAULT_SETTINGS.ollama_primary_url),
        fallback_client=OllamaClient(DEFAULT_SETTINGS.ollama_fallback_url),
    )


def handle_command(payload: dict) -> dict:
    cmd = payload.get("cmd")
    if cmd == "ping":
        return {"ok": True, "reply": "pong"}
    if cmd == "run":
        if payload.get("language") != "python":
            return {"ok": False, "error": "unsupported_language"}
        return run_python_in_docker(payload.get("code", ""))
    if cmd == "chat":
        routed = _build_router().route_chat(payload.get("message", ""))
        return {"ok": True, **routed}
    if cmd == "get_phase_1_status":
        return {"ok": True, "status": get_phase_1_status()}
    return {"ok": False, "error": "unknown_command"}


class NDJSONRequestHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        while True:
            raw = self.rfile.readline()
            if not raw:
                break
            try:
                decoded = raw.decode("utf-8")
            except UnicodeDecodeError:
                self._send({"ok": False, "error": "invalid_encoding"})
                continue
            line = decoded.strip()
            if not line:
                self._send({"ok": False, "error": "empty_message"})
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                self._send({"ok": False, "error": "invalid_json"})
                continue
            if not isinstance(payload, dict):
                self._send({"ok": False, "error": "invalid_message_type"})
                continue
            self._send(handle_command(payload))

    def _send(self, body: dict) -> None:
        self.wfile.write((json.dumps(body) + "\n").encode("utf-8"))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


def main() -> None:
    with ThreadedTCPServer((DEFAULT_SETTINGS.tcp_host, DEFAULT_SETTINGS.tcp_port), NDJSONRequestHandler) as server:
        print(f"Cody TCP server listening on {DEFAULT_SETTINGS.tcp_host}:{DEFAULT_SETTINGS.tcp_port}")
        server.serve_forever()


if __name__ == "__main__":
    main()
