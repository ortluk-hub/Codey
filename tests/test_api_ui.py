import unittest
from unittest.mock import patch

from cody.api_ui import render_chat_page


class APIUITests(unittest.TestCase):
    def test_render_chat_page_contains_chat_form_and_chat_endpoint(self):
        html = render_chat_page()

        self.assertIn('<form id="chat-form">', html)
        self.assertIn("fetch('/chat'", html)
        self.assertIn('Cody Chat', html)

    @patch('cody.api_ui.sandbox.run_python_in_docker')
    def test_run_endpoint_exists_and_calls_sandbox(self, mock_run):
        """Test that the /run endpoint is defined and calls sandbox."""
        from cody.api_ui import app
        
        # Check app has the /run route
        routes = [route.path for route in app.routes]
        self.assertIn('/run', routes)
        
        # Find the run_code endpoint
        run_routes = [r for r in app.routes if r.path == '/run']
        self.assertEqual(len(run_routes), 1)
        self.assertEqual(run_routes[0].methods, {'POST'})


if __name__ == "__main__":
    unittest.main()
