import unittest
from unittest.mock import patch, MagicMock

from cody.sandbox import DockerPolicy, run_python_in_docker


class DockerPolicyTests(unittest.TestCase):
    def test_policy_generates_expected_restriction_flags(self):
        flags = DockerPolicy().to_docker_flags()

        self.assertIn("--network", flags)
        self.assertIn("none", flags)
        self.assertIn("--read-only", flags)
        self.assertIn("--cap-drop", flags)
        self.assertIn("ALL", flags)
        self.assertIn("--memory", flags)
        self.assertIn("--pids-limit", flags)

    def test_policy_has_increased_timeout_for_complex_code(self):
        policy = DockerPolicy()
        self.assertEqual(policy.timeout_seconds, 30)

    def test_policy_default_values_are_secure(self):
        policy = DockerPolicy()
        
        self.assertEqual(policy.image, "python:3.12-alpine")
        self.assertEqual(policy.memory, "128m")
        self.assertEqual(policy.cpus, "0.5")
        self.assertEqual(policy.pids_limit, 64)
        self.assertEqual(policy.user, "65534:65534")
        self.assertTrue(policy.network_none)
        self.assertTrue(policy.read_only)
        self.assertTrue(policy.cap_drop_all)


class RunPythonInDockerTests(unittest.TestCase):
    @patch('cody.sandbox.subprocess.run')
    def test_run_python_in_docker_returns_output(self, mock_run):
        mock_run.return_value = MagicMock(
            stdout="hello\n",
            stderr="",
            returncode=0
        )
        
        result = run_python_in_docker("print('hello')")
        
        self.assertTrue(result["ok"])
        self.assertEqual(result["stdout"], "hello\n")
        self.assertEqual(result["exit_code"], 0)

    @patch('cody.sandbox.subprocess.run')
    def test_run_python_in_docker_handles_timeout(self, mock_run):
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired("cmd", 30)
        
        result = run_python_in_docker("print('slow')")
        
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "sandbox_timeout")

    @patch('cody.sandbox.subprocess.run')
    def test_run_python_in_docker_handles_docker_not_found(self, mock_run):
        mock_run.side_effect = FileNotFoundError()
        
        result = run_python_in_docker("print('hello')")
        
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "docker_not_available")


if __name__ == "__main__":
    unittest.main()
