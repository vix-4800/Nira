from unittest.mock import MagicMock, patch

# fmt: off
# isort: off
from agent.tools.scrape_url_tool import scrape_url_tool
from agent.tools.researcher.summarize_text_tool import summarize_text_tool
# isort: on
# fmt: on


class TestScrapeURLTool:
    def test_summarize_text(self):
        summary = summarize_text_tool.func(text="One. Two. Three.", sentences=2)
        assert summary == "One. Two."

    @patch("agent.tools.scrape_url_tool.requests.get")
    def test_scrape_url(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = "<html><body><p>First sentence. Second sentence. Third sentence.</p></body></html>"
        mock_resp.raise_for_status = lambda: None
        mock_get.return_value = mock_resp

        messages = []

        from contextlib import contextmanager

        @contextmanager
        def fake_status(msg):
            messages.append(msg)
            yield

        with patch("agent.tools.scrape_url_tool.status_manager.status", fake_status):
            text = scrape_url_tool.func("https://example.com")

        assert "First sentence." in text
        assert "читаю страницу" in messages[0]
