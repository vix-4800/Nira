import unittest
from unittest.mock import patch

from agent.tools.get_repo_info_tool import get_repo_info_tool


class GitHubToolTest(unittest.TestCase):
    @patch("agent.tools.get_repo_info_tool.requests.get")
    def test_get_repo_info_success(self, mock_get):
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = {
            "full_name": "octocat/Hello-World",
            "stargazers_count": 5,
            "forks_count": 2,
        }
        result = get_repo_info_tool("octocat/Hello-World")
        self.assertIn("octocat/Hello-World", result)
        mock_get.assert_called_once()

    @patch("agent.tools.get_repo_info_tool.requests.get", side_effect=Exception("fail"))
    def test_get_repo_info_error(self, mock_get):
        result = get_repo_info_tool("octocat/Hello-World")
        self.assertIn("Failed to fetch", result)


if __name__ == "__main__":
    unittest.main()
