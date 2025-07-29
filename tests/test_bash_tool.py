import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agent.tools.run_bash_command_tool import _is_dangerous, run_bash_command_tool


class BashToolTest(unittest.TestCase):
    def test_is_dangerous(self):
        self.assertTrue(_is_dangerous("rm -rf /"))
        self.assertFalse(_is_dangerous("ls"))

    @patch("builtins.input", return_value="y")
    def test_run_safe_command_confirm(self, mock_input):
        out = run_bash_command_tool("echo hello")
        self.assertEqual(out.strip(), "hello")

    @patch("builtins.input", return_value="n")
    def test_cancel_command(self, mock_input):
        result = run_bash_command_tool("echo hi")
        self.assertEqual(result, "Команда отменена")

    @patch("subprocess.run")
    @patch("builtins.input", return_value="y")
    def test_dangerous_with_auto_confirm(self, mock_input, mock_run):
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        os.environ["AUTO_CONFIRM"] = "true"
        out = run_bash_command_tool("rm -rf tmp")
        self.assertEqual(out, "(Пустой вывод)")
        del os.environ["AUTO_CONFIRM"]


if __name__ == "__main__":
    unittest.main()
