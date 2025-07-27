import unittest
from unittest.mock import patch
import requests

import main
from main import ask_llm, LLMServerUnavailable, check_command_error


class AskLLMTests(unittest.TestCase):
    @patch("requests.post")
    def test_connection_error_raises(self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError
        main.server_url = "http://localhost"
        main.model = "test-model"
        with self.assertRaises(LLMServerUnavailable):
            ask_llm("hi", "http://localhost", "model")

    @patch("requests.post")
    def test_timeout_passed_to_requests(self, mock_post):
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"response": "ok"}
        mock_post.return_value = mock_response

        ask_llm("hi", "http://localhost", "model", timeout=5)

        mock_post.assert_called_with(
            "http://localhost/api/generate",
            json={"model": "model", "prompt": "hi", "stream": False},
            timeout=5,
        )


class CheckCommandErrorTests(unittest.TestCase):
    def test_case_insensitive(self):
        self.assertTrue(check_command_error("SyNtAx ErRoR somewhere"))


if __name__ == "__main__":
    unittest.main()
