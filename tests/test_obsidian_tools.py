import tempfile
from pathlib import Path
from unittest import mock

import pytest

from agent.core.config import load_config
from agent.tools.obsidian_manager_tool import obsidian_manager


class TestObsidianTools:
    def setup_method(self):
        load_config.cache_clear()
        self.tempdir = tempfile.TemporaryDirectory()
        self.vault = Path(self.tempdir.name)

    def teardown_method(self):
        self.tempdir.cleanup()

    def test_create_and_summarize_note(self):
        with mock.patch.dict("os.environ", {"OBSIDIAN_VAULT": str(self.vault)}):
            result = obsidian_manager.func(
                "create_note",
                title="Test",
                content="Hello world. More text.",
            )
            assert "Created" in result
            summary = obsidian_manager.func("summarize_note", title="Test", sentences=1)
            assert summary == "Hello world."

    def test_missing_vault(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            with pytest.raises(RuntimeError):
                obsidian_manager.func("create_note", title="Foo")
