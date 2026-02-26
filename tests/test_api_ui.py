import unittest

from cody.api_ui import render_chat_page


class APIUITests(unittest.TestCase):
    def test_render_chat_page_contains_chat_form_and_chat_endpoint(self):
        html = render_chat_page()

        self.assertIn('<form id="chat-form">', html)
        self.assertIn("fetch('/chat'", html)
        self.assertIn('Cody Chat', html)


if __name__ == "__main__":
    unittest.main()
