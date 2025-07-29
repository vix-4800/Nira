import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent.tools.pdf_tools import (
    extract_text_from_pdf,
    summarize_text,
    summarize_pdf,
    count_words_in_file,
)


class PDFToolsTest(unittest.TestCase):
    def test_extract_text_from_pdf(self):
        text = extract_text_from_pdf('tests/sample.pdf')
        self.assertIn('Hello world', text)

    def test_summarize_text(self):
        summary = summarize_text('One. Two. Three. Four.', sentences=2)
        self.assertEqual(summary, 'One. Two.')

    def test_summarize_pdf(self):
        summary = summarize_pdf('tests/sample.pdf', sentences=1)
        self.assertTrue(summary.startswith('Hello world'))

    def test_count_words_in_file(self):
        with tempfile.NamedTemporaryFile('w+', delete=False) as f:
            f.write('hello world here')
            path = f.name
        try:
            count = count_words_in_file(path)
            self.assertEqual(count, '3')
        finally:
            os.remove(path)


if __name__ == '__main__':
    unittest.main()
