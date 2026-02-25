import unittest

from codey import get_agent_architecture


class AgentArchitectureTests(unittest.TestCase):
    def test_architecture_is_modular_and_coder_focused(self):
        architecture = get_agent_architecture()

        self.assertEqual(architecture.name, "Cody")
        self.assertTrue(architecture.modular)
        self.assertIn("coder agent", architecture.mission.lower())

    def test_models_match_requested_stack(self):
        architecture = get_agent_architecture()

        self.assertEqual(architecture.intent_resolver.model, "ollama-local-tiny")
        self.assertEqual(architecture.primary_llm.model, "ollama-cloud")
        self.assertEqual(architecture.fallback_llm.model, "ollama-local")
        self.assertEqual(architecture.primary_llm.served_via, "ollama")
        self.assertEqual(architecture.fallback_llm.served_via, "ollama")

    def test_runtime_memory_and_communication_policies_match_requirements(self):
        architecture = get_agent_architecture()

        self.assertTrue(architecture.runtime_policy.tools_available)
        self.assertEqual(
            architecture.runtime_policy.filesystem_access,
            "containerized_sandbox",
        )
        self.assertEqual(architecture.runtime_policy.code_execution_environment, "docker")
        self.assertEqual(
            architecture.memory.short_term,
            "full_context_window",
        )
        self.assertEqual(
            architecture.memory.long_term,
            "summarized_memory",
        )
        self.assertEqual(architecture.communication.tcp_port, 8888)
        self.assertEqual(
            architecture.communication.web_ui,
            "fastapi_chat_with_provider_badges",
        )


if __name__ == "__main__":
    unittest.main()
