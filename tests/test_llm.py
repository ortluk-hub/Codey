import unittest

from cody.llm import LLMRouter, OllamaClient


class _RaisingClient(OllamaClient):
    def chat(self, message: str, model: str) -> str | None:
        raise AttributeError("malformed payload")


class _ReplyingClient(OllamaClient):
    def __init__(self, reply: str):
        super().__init__(endpoint=None)
        self._reply = reply

    def chat(self, message: str, model: str) -> str | None:
        return self._reply


class LLMRouterTests(unittest.TestCase):
    def test_route_chat_falls_back_when_primary_raises(self):
        router = LLMRouter(
            intent_client=OllamaClient(endpoint=None),
            primary_client=_RaisingClient(endpoint="http://example"),
            fallback_client=_ReplyingClient("fallback reply"),
        )

        routed = router.route_chat("hello")

        self.assertEqual(routed["provider"], "ollama-local")
        self.assertEqual(routed["reply"], "fallback reply")

    def test_route_chat_returns_stub_when_all_providers_fail(self):
        router = LLMRouter(
            intent_client=OllamaClient(endpoint=None),
            primary_client=_RaisingClient(endpoint="http://example"),
            fallback_client=_RaisingClient(endpoint="http://example"),
        )

        routed = router.route_chat("hello")

        self.assertEqual(routed["provider"], "stub")
        self.assertIn("[stub] Cody received: hello", routed["reply"])


if __name__ == "__main__":
    unittest.main()
