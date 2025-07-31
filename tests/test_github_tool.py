from unittest.mock import patch


from agent.core.config import load_config
from agent.tools.coder.github_manager_tool import github_manager


class TestGitHubTool:
    def setup_method(self):
        load_config.cache_clear()

    @patch("agent.tools.coder.github_manager_tool.request_json")
    def test_get_repo_info_success(self, mock_get):
        mock_get.return_value = {
            "full_name": "octocat/Hello-World",
            "stargazers_count": 5,
            "forks_count": 2,
        }
        result = github_manager.func("repo_info", repo="octocat/Hello-World")
        assert isinstance(result, dict)
        assert result["full_name"] == "octocat/Hello-World"
        mock_get.assert_called_once()

    @patch(
        "agent.tools.coder.github_manager_tool.request_json",
        return_value="Failed to fetch repo info: fail",
    )
    def test_get_repo_info_error(self, mock_get):
        result = github_manager.func("repo_info", repo="octocat/Hello-World")
        assert "Failed to fetch" in result

    @patch("agent.tools.coder.github_manager_tool.request_json")
    def test_create_repo_success(self, mock_post):
        mock_post.return_value = {"name": "new"}
        with patch.dict("os.environ", {"GITHUB_TOKEN": "t"}):
            result = github_manager.func("create_repo", repo="new")
        assert isinstance(result, dict)
        assert result["name"] == "new"
        mock_post.assert_called_once()

    @patch(
        "agent.tools.coder.github_manager_tool.request_json",
        return_value="Failed to create repo: fail",
    )
    def test_create_repo_error(self, mock_post):
        with patch.dict("os.environ", {"GITHUB_TOKEN": "t"}):
            result = github_manager.func("create_repo", repo="new")
        assert "Failed to create repo" in result

    @patch("agent.tools.coder.github_manager_tool.request_json")
    def test_create_issue_success(self, mock_post):
        mock_post.return_value = {"title": "bug"}
        with patch.dict("os.environ", {"GITHUB_TOKEN": "t"}):
            result = github_manager.func(
                "create_issue", repo="octocat/Hello-World", title="bug"
            )
        assert result["title"] == "bug"
        mock_post.assert_called_once()

    @patch("agent.tools.coder.github_manager_tool.request_json")
    def test_create_pr_success(self, mock_post):
        mock_post.return_value = {"title": "pr"}
        with patch.dict("os.environ", {"GITHUB_TOKEN": "t"}):
            result = github_manager.func(
                "create_pr",
                repo="octocat/Hello-World",
                title="pr",
                head="feat",
                base="main",
            )
        assert result["title"] == "pr"
        mock_post.assert_called_once()
