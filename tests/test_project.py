import unittest

from codey import get_agent_architecture


class AgentArchitectureTests(unittest.TestCase):
    def test_architecture_is_modular_and_coding_focused(self):
        architecture = get_agent_architecture()

        self.assertEqual(architecture.name, "Cody")
        self.assertTrue(architecture.modular)
        self.assertIn("coding agent", architecture.mission.lower())

    def test_models_match_requested_stack(self):
        architecture = get_agent_architecture()

        self.assertEqual(architecture.primary_llm.model, "qwen3-coder:480b-cloud")
        self.assertEqual(architecture.fallback_llm.model, "qwen2.5:1.5b")
        self.assertEqual(architecture.primary_llm.served_via, "ollama")
        self.assertEqual(architecture.fallback_llm.served_via, "ollama")

    def test_runtime_and_memory_policy_match_requirements(self):
        architecture = get_agent_architecture()

        self.assertTrue(architecture.runtime_policy.tools_available)
        self.assertEqual(
            architecture.runtime_policy.filesystem_access,
            "containerized_sandbox",
        )
        self.assertEqual(
            architecture.memory.short_term,
            "full_context_window",
        )
        self.assertEqual(
            architecture.memory.long_term,
            "summarized_memory",
        )


if __name__ == "__main__":
    unittest.main()
