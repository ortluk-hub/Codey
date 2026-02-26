import unittest

from cody.llm import LLMRouter


class StubClient:
    def __init__(self, response=None):
        self.response = response
        self.calls = []

    def chat(self, message: str, model: str):
        self.calls.append({"message": message, "model": model})
        return self.response


class LLMRouterTests(unittest.TestCase):
    def test_stub_queues_message_when_providers_unavailable(self):
        router = LLMRouter(
            intent_client=StubClient(),
            primary_client=StubClient(response=None),
            fallback_client=StubClient(response=None),
        )

        response = router.route_chat("hello")

        self.assertEqual(response["provider"], "stub")
        self.assertTrue(response["queued"])
        self.assertEqual(response["queued_messages"], 1)
        self.assertEqual(router.pending_messages, ["hello"])

    def test_queued_messages_are_replayed_and_cleared_when_provider_recovers(self):
        primary_client = StubClient(response=None)
        fallback_client = StubClient(response=None)
        router = LLMRouter(
            intent_client=StubClient(),
            primary_client=primary_client,
            fallback_client=fallback_client,
        )

        router.route_chat("first")
        router.route_chat("second")

        fallback_client.response = "Recovered response"
        response = router.route_chat("third")

        self.assertEqual(response["provider"], "ollama-local")
        self.assertEqual(response["reply"], "Recovered response")
        self.assertEqual(router.pending_messages, [])

        latest_payload = fallback_client.calls[-1]["message"]
        self.assertIn("Queued messages:", latest_payload)
        self.assertIn("- first", latest_payload)
        self.assertIn("- second", latest_payload)
        self.assertIn("Latest user message:\nthird", latest_payload)


if __name__ == "__main__":
    unittest.main()
