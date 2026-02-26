import json
import socket
import threading
import unittest

from cody.tcp_server import NDJSONRequestHandler, ThreadedTCPServer, handle_command


class StubRouter:
    def __init__(self, reply: str, provider: str = "stub"):
        self.reply = reply
        self.provider = provider
        self.calls = []

    def route_chat(self, message: str) -> dict:
        self.calls.append(message)
        return {"reply": self.reply, "provider": self.provider}


class TCPProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadedTCPServer(("127.0.0.1", 0), NDJSONRequestHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def _send_line(self, line: bytes) -> dict:
        with socket.create_connection(("127.0.0.1", self.port), timeout=2) as sock:
            sock.sendall(line)
            response = b""
            while not response.endswith(b"\n"):
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
        return json.loads(response.decode("utf-8"))

    def test_ping_command(self):
        response = self._send_line(b'{"cmd":"ping"}\n')
        self.assertEqual(response, {"ok": True, "reply": "pong"})

    def test_phase_2_status_command(self):
        response = self._send_line(b'{"cmd":"get_phase_2_status"}\n')
        self.assertTrue(response["ok"])
        self.assertIn("status", response)
        self.assertIn("tooling_contract_expanded", response["status"])

    def test_phase_3_status_command(self):
        response = self._send_line(b'{"cmd":"get_phase_3_status"}\n')
        self.assertTrue(response["ok"])
        self.assertIn("status", response)
        self.assertIn("tcp_contract_supports_phase_3", response["status"])

    def test_invalid_json_framing(self):
        response = self._send_line(b'{"cmd":"ping"\n')
        self.assertEqual(response["ok"], False)
        self.assertEqual(response["error"], "invalid_json")

    def test_chat_uses_provided_router_instance(self):
        router_a = StubRouter(reply="a")
        router_b = StubRouter(reply="b")

        response_a = handle_command({"cmd": "chat", "message": "hello from a"}, router=router_a)
        response_b = handle_command({"cmd": "chat", "message": "hello from b"}, router=router_b)

        self.assertEqual(response_a, {"ok": True, "reply": "a", "provider": "stub"})
        self.assertEqual(response_b, {"ok": True, "reply": "b", "provider": "stub"})
        self.assertEqual(router_a.calls, ["hello from a"])
        self.assertEqual(router_b.calls, ["hello from b"])


if __name__ == "__main__":
    unittest.main()
