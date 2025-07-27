import unittest
from unittest.mock import patch, mock_open
import io
import json
import requests
import os

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


class LoadPromptDataTests(unittest.TestCase):
    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("sys.exit")
    def test_file_not_found_exits(self, mock_exit, mock_open_fn):
        main.load_prompt_data("missing.json")
        mock_exit.assert_called_once()
        self.assertNotEqual(mock_exit.call_args[0][0], 0)

    @patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0))
    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    @patch("sys.exit")
    def test_json_error_exits(self, mock_exit, mock_open_fn, mock_json):
        main.load_prompt_data("bad.json")
        mock_exit.assert_called_once()
        self.assertNotEqual(mock_exit.call_args[0][0], 0)


class ParseEnvTests(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_defaults(self):
        server, model, auto = main.parse_env()
        self.assertEqual(server, main.DEFAULT_SERVER)
        self.assertEqual(model, main.DEFAULT_MODEL)
        self.assertFalse(auto)

    @patch.dict(os.environ, {"SERVER": "s", "MODEL": "m", "AUTO_CONFIRM": "true"}, clear=True)
    def test_custom(self):
        server, model, auto = main.parse_env()
        self.assertEqual(server, "s")
        self.assertEqual(model, "m")
        self.assertTrue(auto)

    @patch.dict(os.environ, {"AUTO_CONFIRM": "no"}, clear=True)
    def test_false(self):
        _, _, auto = main.parse_env()
        self.assertFalse(auto)


if __name__ == "__main__":
    unittest.main()
