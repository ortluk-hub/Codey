import unittest

from cody.llm import LLMRouter, ToolExecutor, extract_code_block


class StubClient:
    def __init__(self, response=None):
        self.response = response
        self.calls = []

    def chat(self, message: str, model: str):
        self.calls.append({"message": message, "model": model})
        return self.response


class StubSandbox:
    def __init__(self, result=None):
        self.result = result or {"ok": True, "stdout": "42\n", "stderr": "", "exit_code": 0}
        self.calls = []

    def run_python_in_docker(self, code: str):
        self.calls.append({"code": code})
        return self.result


class ExtractCodeBlockTests(unittest.TestCase):
    def test_extract_code_block_from_python_markdown(self):
        text = "Here's the code:\n```python\nprint(42)\n```"
        code = extract_code_block(text)
        self.assertEqual(code, "print(42)")

    def test_extract_code_block_from_plain_markdown(self):
        text = "Here's the code:\n```\nprint(42)\n```"
        code = extract_code_block(text)
        self.assertEqual(code, "print(42)")

    def test_extract_code_block_returns_none_for_no_code(self):
        text = "No code here"
        code = extract_code_block(text)
        self.assertIsNone(code)


class ToolExecutorTests(unittest.TestCase):
    def test_execute_python_logs_and_returns_result(self):
        sandbox = StubSandbox({"ok": True, "stdout": "hello\n", "stderr": "", "exit_code": 0})
        executor = ToolExecutor()
        # Patch the sandbox module
        import cody.llm
        original_sandbox = cody.llm.sandbox
        cody.llm.sandbox = sandbox
        
        try:
            result = executor.execute_python("print('hello')", "req-123")
            self.assertEqual(result["ok"], True)
            self.assertEqual(result["stdout"], "hello\n")
            self.assertEqual(len(sandbox.calls), 1)
            self.assertEqual(sandbox.calls[0]["code"], "print('hello')")
        finally:
            cody.llm.sandbox = original_sandbox


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

    def test_route_chat_logs_request_lifecycle_with_provider_and_recipient(self):
        router = LLMRouter(
            intent_client=StubClient(),
            primary_client=StubClient(response="ok"),
            fallback_client=StubClient(response=None),
        )

        with self.assertLogs("cody.llm", level="INFO") as captured:
            response = router.route_chat("hello", request_id="req-123", recipient="api-http")

        self.assertEqual(response["provider"], "ollama-cloud")
        joined = "\n".join(captured.output)
        self.assertIn("llm.request.received request_id=req-123 recipient=api-http", joined)
        self.assertIn("llm.call.start request_id=req-123 provider=ollama-cloud", joined)
        self.assertIn("llm.call.success request_id=req-123 provider=ollama-cloud", joined)
        self.assertIn("llm.response.sent request_id=req-123 recipient=api-http provider=ollama-cloud", joined)

    def test_resolve_intent_detects_math_expression_with_operators(self):
        router = LLMRouter(
            intent_client=StubClient(),
            primary_client=StubClient(response=None),
            fallback_client=StubClient(response=None),
        )

        code, can_handle = router._resolve_intent("What is 2 + 2 * 10?", "req-123")

        self.assertTrue(can_handle)
        self.assertEqual(code, "print(2 + 2 * 10)")

    def test_resolve_intent_detects_divided_by_pattern(self):
        router = LLMRouter(
            intent_client=StubClient(),
            primary_client=StubClient(response=None),
            fallback_client=StubClient(response=None),
        )

        code, can_handle = router._resolve_intent("What is 100 divided by 4?", "req-123")

        self.assertTrue(can_handle)
        self.assertEqual(code, "print(100 / 4)")

    def test_resolve_intent_routes_to_llm_for_explanation_requests(self):
        router = LLMRouter(
            intent_client=StubClient(),
            primary_client=StubClient(response=None),
            fallback_client=StubClient(response=None),
        )

        prompt, can_handle = router._resolve_intent("Explain what a decorator is", "req-123")

        self.assertFalse(can_handle)
        self.assertIn("coding assistant", prompt)

    def test_route_chat_executes_tool_for_math_questions(self):
        sandbox = StubSandbox({"ok": True, "stdout": "22\n", "stderr": "", "exit_code": 0})
        router = LLMRouter(
            intent_client=StubClient(),
            primary_client=StubClient(response=None),
            fallback_client=StubClient(response=None),
        )
        # Patch sandbox
        import cody.llm
        original_sandbox = cody.llm.sandbox
        cody.llm.sandbox = sandbox
        
        try:
            response = router.route_chat("What is 2 + 2 * 10?", request_id="req-123")
            self.assertEqual(response["provider"], "local-tool")
            self.assertIn("22", response["reply"])
            self.assertEqual(response["executed_code"], "print(2 + 2 * 10)")
        finally:
            cody.llm.sandbox = original_sandbox

    def test_route_chat_uses_cloud_for_non_math_requests(self):
        router = LLMRouter(
            intent_client=StubClient(),
            primary_client=StubClient(response="Cloud response"),
            fallback_client=StubClient(response=None),
        )

        response = router.route_chat("Explain decorators", request_id="req-123")

        self.assertEqual(response["provider"], "ollama-cloud")
        self.assertEqual(response["reply"], "Cloud response")


if __name__ == "__main__":
    unittest.main()
