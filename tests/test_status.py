import os
import tempfile
import unittest

from cody.status import get_phase_1_status


class StatusTests(unittest.TestCase):
    def test_phase_1_status_independent_of_working_directory(self):
        original_cwd = os.getcwd()
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                os.chdir(temp_dir)
                status = get_phase_1_status()
        finally:
            os.chdir(original_cwd)

        self.assertTrue(status["architecture_metadata_versioned"])

    def test_phase_1_status_shape(self):
        status = get_phase_1_status()

        self.assertIn("tcp_contract_locked", status)
        self.assertIn("docker_policy_validated", status)
        self.assertIn("architecture_metadata_versioned", status)
        self.assertIn("complete", status)

        self.assertIsInstance(status["tcp_contract_locked"], bool)
        self.assertIsInstance(status["docker_policy_validated"], bool)
        self.assertIsInstance(status["architecture_metadata_versioned"], bool)
        self.assertEqual(
            status["complete"],
            status["tcp_contract_locked"]
            and status["docker_policy_validated"]
            and status["architecture_metadata_versioned"],
        )


if __name__ == "__main__":
    unittest.main()
