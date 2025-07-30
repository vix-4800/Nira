import os
import sys
import tempfile
import unittest
from pathlib import Path

from agent.tools.file_manager_tool import file_manager
from agent.tools.pdf_manager_tool import pdf_manager
from agent.tools.summarise_text_tool import summarise_text_tool

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


class PDFToolsTest(unittest.TestCase):
    def test_extract_text_from_pdf(self):
        text = pdf_manager.func("extract_text", path="tests/sample.pdf")
        self.assertIn("Hello world", text)

    def test_summarize_text(self):
        summary = summarise_text_tool.func(text="One. Two. Three. Four.", sentences=2)
        self.assertEqual(summary, "One. Two.")

    def test_summarize_pdf(self):
        summary = pdf_manager.func("summarize", path="tests/sample.pdf", sentences=1)
        self.assertTrue(summary.startswith("Hello world"))

    def test_count_words_in_file(self):
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            f.write("hello world here")
            path = f.name
        try:
            count = file_manager.func("count_words", path=path)
            self.assertEqual(count, "3")
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
