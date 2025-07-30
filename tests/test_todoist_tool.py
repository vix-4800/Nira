import unittest
from unittest.mock import patch

from agent.tools.todoist_manager_tool import todoist_manager


class TodoistToolTest(unittest.TestCase):
    @patch("agent.tools.todoist_manager_tool.requests.get")
    def test_list_tasks_success(self, mock_get):
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = [{"id": "1", "content": "task"}]
        with patch.dict("os.environ", {"TODOIST_TOKEN": "token"}):
            result = todoist_manager.func("list_tasks")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["content"], "task")
        mock_get.assert_called_once()

    @patch("agent.tools.todoist_manager_tool.requests.post", side_effect=Exception("fail"))
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
