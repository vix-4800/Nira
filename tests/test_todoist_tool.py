import unittest
from unittest.mock import patch

from agent.core.config import load_config
from agent.tools.todoist_manager_tool import todoist_manager


class TodoistToolTest(unittest.TestCase):
    def setUp(self):
        load_config.cache_clear()

    @patch("agent.tools.todoist_manager_tool.request_json")
    def test_list_tasks_success(self, mock_get):
        mock_get.return_value = [{"id": "1", "content": "task"}]
        with patch.dict("os.environ", {"TODOIST_TOKEN": "token"}):
            result = todoist_manager.func("list_tasks")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["content"], "task")
        mock_get.assert_called_once()

    @patch(
        "agent.tools.todoist_manager_tool.request_json",
        return_value="Failed to create task: fail",
    )
    def test_create_task_error(self, mock_post):
        with patch.dict("os.environ", {"TODOIST_TOKEN": "token"}):
            result = todoist_manager.func("create_task", content="hi")
        self.assertIn("Failed to create task", result)

    def test_missing_token(self):
        with patch.dict("os.environ", {}, clear=True):
            result = todoist_manager.func("list_tasks")
        self.assertIn("not configured", result)


if __name__ == "__main__":
    unittest.main()
