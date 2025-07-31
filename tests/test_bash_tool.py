import os
import unittest
from unittest.mock import patch

# fmt: off
# isort: off
from agent.tools.sysops.run_bash_command_tool import (
    _is_dangerous,
    run_bash_command_tool,
)
# isort: on
# fmt: on


class BashToolTest(unittest.TestCase):
    def test_is_dangerous(self):
        self.assertTrue(_is_dangerous("rm -rf /"))
        self.assertTrue(_is_dangerous("poweroff"))
        self.assertTrue(_is_dangerous("init 0"))
        self.assertFalse(_is_dangerous("ls"))

    @patch("builtins.input", return_value="y")
    def test_run_safe_command_confirm(self, mock_input):
        out = run_bash_command_tool.func("echo hello")
        self.assertEqual(out.strip(), "hello")

    @patch("builtins.input", return_value="n")
    def test_cancel_command(self, mock_input):
        result = run_bash_command_tool.func("echo hi")
        self.assertEqual(result, "Команда отменена")

    @patch("subprocess.run")
    @patch("builtins.input", return_value="y")
    def test_dangerous_with_auto_confirm(self, mock_input, mock_run):
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        os.environ["AUTO_CONFIRM"] = "true"
        out = run_bash_command_tool.func("rm -rf tmp")
        self.assertEqual(out, "(Пустой вывод)")
        del os.environ["AUTO_CONFIRM"]

    @patch("builtins.input", return_value="n")
    def test_status_during_confirmation(self, mock_input):
        messages = []

        from contextlib import contextmanager

        @contextmanager
        def fake_status(msg):
            messages.append(msg)
            yield

        with patch(
            "agent.tools.sysops.run_bash_command_tool.status_manager.status", fake_status
        ):
            result = run_bash_command_tool.func("rm -rf tmp")

        self.assertEqual(result, "Команда отменена")
        self.assertIn("ожидаю подтверждения", messages[0])


if __name__ == "__main__":
    unittest.main()
