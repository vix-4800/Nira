import unittest
from unittest.mock import MagicMock, patch

from agent.tools.summarize_website_tool import summarize_text, summarize_website_tool


class WebsiteToolTest(unittest.TestCase):
    def test_summarize_text(self):
        summary = summarize_text("One. Two. Three.", sentences=2)
        self.assertEqual(summary, "One. Two.")

    @patch("agent.tools.summarize_website_tool.requests.get")
    def test_summarize_website(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = "<html><body><p>First sentence. Second sentence. Third sentence.</p></body></html>"
        mock_resp.raise_for_status = lambda: None
        mock_get.return_value = mock_resp

        summary = summarize_website_tool.func("https://example.com", sentences=2)
        self.assertEqual(summary, "First sentence. Second sentence.")


if __name__ == "__main__":
    unittest.main()
