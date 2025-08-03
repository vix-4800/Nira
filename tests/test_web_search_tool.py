from unittest.mock import patch

from agent.tools.researcher.web_search_tool import web_search_tool


class FakeDDGS:
    last_instance = None

    def __enter__(self):
        FakeDDGS.last_instance = self
        self.closed = False
        return self

    def __exit__(self, exc_type, exc, tb):
        self.closed = True

    def text(self, query, safesearch="off", max_results=5):
        self.last_call = (query, safesearch, max_results)

        def generator():
            if self.closed:
                raise RuntimeError("DDGS instance is closed")
            yield {"title": "Example", "href": "https://example.com", "body": "Test"}

        return generator()


class TestWebSearchTool:
    @patch("agent.tools.researcher.web_search_tool.DDGS", FakeDDGS)
    def test_web_search(self):
        result = web_search_tool.func("example", max_results=1)
        assert "Example" in result
        assert "https://example.com" in result
        assert FakeDDGS.last_instance.last_call == ("example", "off", 1)
        assert FakeDDGS.last_instance.closed is True
