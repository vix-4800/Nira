import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent.tools.obsidian_manager_tool import obsidian_manager
from agent.core.config import load_config


class ObsidianToolsTest(unittest.TestCase):
    def setUp(self):
        load_config.cache_clear()
        self.tempdir = tempfile.TemporaryDirectory()
        self.vault = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_create_and_summarize_note(self):
        with mock.patch.dict("os.environ", {"OBSIDIAN_VAULT": str(self.vault)}):
            result = obsidian_manager.func(
                "create_note",
                title="Test",
                content="Hello world. More text.",
            )
            self.assertIn("Created", result)
            summary = obsidian_manager.func("summarize_note", title="Test", sentences=1)
            self.assertEqual(summary, "Hello world.")

    def test_missing_vault(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(RuntimeError):
                obsidian_manager.func("create_note", title="Foo")


if __name__ == "__main__":
    unittest.main()
