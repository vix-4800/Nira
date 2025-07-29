import tempfile
import unittest
from unittest import mock
from pathlib import Path
from agent.tools.create_note_tool import create_note
from agent.tools.summarize_note_tool import summarize_note

class ObsidianToolsTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.vault = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_create_and_summarize_note(self):
        with mock.patch.dict('os.environ', {'OBSIDIAN_VAULT': str(self.vault)}):
            result = create_note('Test', 'Hello world. More text.')
            self.assertIn('Created', result)
            summary = summarize_note('Test', sentences=1)
            self.assertEqual(summary, 'Hello world.')

    def test_missing_vault(self):
        with mock.patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(RuntimeError):
                create_note('Foo')

if __name__ == '__main__':
    unittest.main()
