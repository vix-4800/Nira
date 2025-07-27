import unittest
from unittest.mock import patch, mock_open
import io
import json
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


if __name__ == "__main__":
    unittest.main()
