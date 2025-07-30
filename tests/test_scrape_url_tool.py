import unittest
from unittest.mock import MagicMock, patch

# fmt: off
# isort: off
from agent.tools.scrape_url_tool import scrape_url_tool
from agent.tools.summarise_text_tool import summarise_text
# isort: on
# fmt: on


class ScrapeURLToolTest(unittest.TestCase):
    def test_summarize_text(self):
        summary = summarise_text("One. Two. Three.", sentences=2)
        self.assertEqual(summary, "One. Two.")

    @patch("agent.tools.scrape_url_tool.requests.get")
    def test_scrape_url(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = "<html><body><p>First sentence. Second sentence. Third sentence.</p></body></html>"
        mock_resp.raise_for_status = lambda: None
        mock_get.return_value = mock_resp

        text = scrape_url_tool.func("https://example.com")
        self.assertIn("First sentence.", text)


if __name__ == "__main__":
    unittest.main()
