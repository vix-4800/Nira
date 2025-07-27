import unittest
from unittest.mock import patch, mock_open
import io
import json
import requests
import os
from types import SimpleNamespace

import main
from main import ask_llm, LLMServerUnavailable, check_command_error, is_command_safe, main as main_entry


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


class IsCommandSafeTests(unittest.TestCase):
    def test_dangerous_patterns(self):
        self.assertFalse(is_command_safe("rm -rf /"))
        self.assertFalse(is_command_safe("shutdown -h now"))

    def test_harmless(self):
        self.assertTrue(is_command_safe("echo hello"))


class MainExecutionSafetyTests(unittest.TestCase):
    def run_main(self, auto=None, safe=True, confirms=("y",)):
        responses = ["COMMAND: echo hi", "done"]

        def fake_ask_llm(*args, **kwargs):
            return responses.pop(0)

        inputs_list = ["task"] + list(confirms) + ["quit"]
        inputs = iter(inputs_list)

        env = {}
        if auto is not None:
            env["AUTO_CONFIRM"] = auto

        with patch.dict(os.environ, env, clear=True), \
             patch("builtins.input", side_effect=lambda _: next(inputs)), \
             patch.object(main, "parse_args", return_value=SimpleNamespace(log_file=None)), \
             patch.object(main, "load_prompt_data", return_value={"system": "", "examples": []}), \
             patch.object(main, "ask_llm", side_effect=fake_ask_llm), \
             patch.object(main, "is_command_safe", return_value=safe), \
             patch.object(main, "run_command", return_value=("", "", 0)) as run_mock, \
             patch.object(main, "check_llm_server", return_value=None):
            main_entry()
            return run_mock.called

    def test_manual_confirmation(self):
        called = self.run_main(auto=None, safe=True, confirms=("y",))
        self.assertTrue(called)

    def test_dangerous_skipped(self):
        called = self.run_main(auto=None, safe=False, confirms=("n",))
        self.assertFalse(called)

    def test_auto_confirm_safe(self):
        called = self.run_main(auto="1", safe=True, confirms=())
        self.assertTrue(called)

    def test_auto_confirm_dangerous_requires_prompt(self):
        called = self.run_main(auto="1", safe=False, confirms=("y",))
        self.assertTrue(called)


if __name__ == "__main__":
    unittest.main()
