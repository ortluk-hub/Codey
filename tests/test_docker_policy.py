import unittest

from cody.sandbox import DockerPolicy


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


if __name__ == "__main__":
    unittest.main()
