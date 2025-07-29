import unittest
from unittest.mock import patch

from agent.tools.web_search_tool import web_search_tool


class WebSearchToolTest(unittest.TestCase):
    @patch("agent.tools.web_search_tool.DDGS.text")
    def test_web_search(self, mock_text):
        mock_text.return_value = [
            {"title": "Example", "href": "https://example.com", "body": "Test"}
        ]
        result = web_search_tool.func("example", max_results=1)
        self.assertIn("Example", result)
        self.assertIn("https://example.com", result)
        mock_text.assert_called_once_with("example", safesearch="off", max_results=1)


if __name__ == "__main__":
    unittest.main()
