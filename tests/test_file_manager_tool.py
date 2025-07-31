import tempfile
import unittest
from pathlib import Path

from agent.tools.file_manager_tool import file_manager


class FileManagerWriteTest(unittest.TestCase):
    def test_write_and_append(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            path = Path(f.name)
        try:
            out = file_manager.func("write", path=str(path), text="hello")
            self.assertIn("Wrote to", out)
            self.assertEqual(path.read_text(encoding="utf-8"), "hello")

            out = file_manager.func("write", path=str(path), text=" world", append=True)
            self.assertIn("Wrote to", out)
            self.assertEqual(path.read_text(encoding="utf-8"), "hello world")
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
