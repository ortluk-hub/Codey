import unittest

from codey import (
    get_agent_architecture,
    get_phase_1_status,
    get_phase_2_status,
    get_roadmap,
)


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


class RoadmapTests(unittest.TestCase):
    def test_roadmap_contains_three_phases_with_actionable_outcomes(self):
        roadmap = get_roadmap()

        self.assertEqual(len(roadmap), 3)
        self.assertTrue(roadmap[0].phase.startswith("Phase 1"))
        self.assertTrue(roadmap[1].phase.startswith("Phase 2"))
        self.assertTrue(roadmap[2].phase.startswith("Phase 3"))

        for milestone in roadmap:
            self.assertGreaterEqual(len(milestone.outcomes), 3)
            for outcome in milestone.outcomes:
                self.assertTrue(outcome.endswith("."))


class PhaseStatusTests(unittest.TestCase):
    def test_phase_1_status_reports_completed_with_expected_checks(self):
        status = get_phase_1_status()

        self.assertEqual(status.phase, "Phase 1: Foundation hardening")
        self.assertTrue(status.completed)
        self.assertEqual(len(status.checks), 3)
        for check in status.checks:
            self.assertNotIn("not fully", check.lower())
            self.assertNotIn("does not", check.lower())
            self.assertNotIn("missing", check.lower())


class Phase2StatusTests(unittest.TestCase):
    def test_phase_2_status_reports_completed_with_expected_checks(self):
        status = get_phase_2_status()

        self.assertEqual(status.phase, "Phase 2: Tooling and memory maturity")
        self.assertTrue(status.completed)
        self.assertEqual(len(status.checks), 3)
        for check in status.checks:
            self.assertNotIn("not fully", check.lower())
            self.assertNotIn("does not", check.lower())
            self.assertNotIn("missing", check.lower())


if __name__ == "__main__":
    unittest.main()
