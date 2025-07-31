import tempfile
from pathlib import Path

from agent.tools.file_manager_tool import file_manager
from agent.tools.pdf_manager_tool import pdf_manager
from agent.tools.researcher.summarize_text_tool import summarize_text_tool


class TestPDFTools:
    def test_extract_text_from_pdf(self):
        text = pdf_manager.func("extract_text", path="tests/sample.pdf")
        assert "Hello world" in text

    def test_summarize_text(self):
        summary = summarize_text_tool.func(text="One. Two. Three. Four.", sentences=2)
        assert summary == "One. Two."

    def test_summarize_pdf(self):
        summary = pdf_manager.func("summarize", path="tests/sample.pdf", sentences=1)
        assert summary.startswith("Hello world")

    def test_count_words_in_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            path = Path(f.name)
        path.write_text("hello world here", encoding="utf-8")
        try:
            count = file_manager.func("count_words", path=str(path))
            assert count == "3"
        finally:
            path.unlink()
