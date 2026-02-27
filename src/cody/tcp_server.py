"""NDJSON TCP server for Cody."""

import json
import socketserver
import uuid

from . import config, llm, sandbox, status


def _build_router() -> llm.LLMRouter:
    return llm.LLMRouter(
        intent_client=llm.OllamaClient(config.DEFAULT_SETTINGS.ollama_intent_url),
        primary_client=llm.OllamaClient(config.DEFAULT_SETTINGS.ollama_primary_url),
        fallback_client=llm.OllamaClient(config.DEFAULT_SETTINGS.ollama_fallback_url),
    )


def handle_command(
    payload: dict,
    router: llm.LLMRouter | None = None,
    request_id: str | None = None,
    recipient: str = "unknown",
) -> dict:
    cmd = payload.get("cmd")
    if cmd == "ping":
        return {"ok": True, "reply": "pong"}
    if cmd == "run":
        if payload.get("language") != "python":
            return {"ok": False, "error": "unsupported_language"}
        return sandbox.run_python_in_docker(payload.get("code", ""))
    if cmd == "chat":
        active_router = router or _build_router()
        routed = active_router.route_chat(
            payload.get("message", ""), request_id=request_id, recipient=recipient
        )
        return {"ok": True, **routed}
    if cmd == "get_phase_1_status":
        return {"ok": True, "status": status.get_phase_1_status()}
    if cmd == "get_phase_2_status":
        return {"ok": True, "status": status.get_phase_2_status()}
    if cmd == "get_phase_3_status":
        return {"ok": True, "status": status.get_phase_3_status()}
    return {"ok": False, "error": "unknown_command"}


class NDJSONRequestHandler(socketserver.StreamRequestHandler):
    def setup(self) -> None:
        super().setup()
        self.router = _build_router()

    def handle(self) -> None:
        while True:
            raw = self.rfile.readline()
            if not raw:
                break

            try:
                decoded = raw.decode("utf-8")
            except UnicodeDecodeError:
                self._send_safe({"ok": False, "error": "invalid_encoding"})
                continue

            line = decoded.strip()
            if not line:
                # Ignore blank lines instead of erroring; clients often send them.
                continue

            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                self._send_safe({"ok": False, "error": "invalid_json"})
                continue

            if not isinstance(payload, dict):
                self._send_safe({"ok": False, "error": "invalid_message_type"})
                continue

            request_id = payload.get("request_id") or uuid.uuid4().hex
            recipient = self.client_address[0] if self.client_address else "tcp-client"
            self._send_safe(
                handle_command(
                    payload,
                    router=self.router,
                    request_id=request_id,
                    recipient=recipient,
                )
            )

    def _send_safe(self, body: dict) -> None:
        try:
            self.wfile.write((json.dumps(body) + "\n").encode("utf-8"))
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            # Client disconnected before reading response; that's fine.
            return


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


def main() -> None:
    with ThreadedTCPServer((config.DEFAULT_SETTINGS.tcp_host, config.DEFAULT_SETTINGS.tcp_port), NDJSONRequestHandler) as server:
        print(f"Cody TCP server listening on {config.DEFAULT_SETTINGS.tcp_host}:{config.DEFAULT_SETTINGS.tcp_port}")
        server.serve_forever()


if __name__ == "__main__":
    main()
