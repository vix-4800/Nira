from unittest.mock import patch


from agent.tools.researcher.web_search_tool import web_search_tool


class TestWebSearchTool:
    @patch("agent.tools.researcher.web_search_tool.DDGS.text")
    def test_web_search(self, mock_text):
        mock_text.return_value = [
            {"title": "Example", "href": "https://example.com", "body": "Test"}
        ]
        result = web_search_tool.func("example", max_results=1)
        assert "Example" in result
        assert "https://example.com" in result
        mock_text.assert_called_once_with("example", safesearch="off", max_results=1)
