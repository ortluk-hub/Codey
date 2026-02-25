import json
import socket
import threading
import unittest

from cody.tcp_server import NDJSONRequestHandler, ThreadedTCPServer


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

    def test_invalid_json_framing(self):
        response = self._send_line(b'{"cmd":"ping"\n')
        self.assertEqual(response["ok"], False)
        self.assertEqual(response["error"], "invalid_json")


if __name__ == "__main__":
    unittest.main()
