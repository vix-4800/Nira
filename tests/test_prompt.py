import io
from pathlib import Path
from unittest.mock import patch

import pytest

from agent.core.prompt import ConfigError, load_prompt


class TestConfigLoader:
    def setup_method(self):
        load_prompt.cache_clear()

    def test_load_prompt_success(self):
        data = load_prompt("prompt.json")
        assert "system" in data
        assert "coder_system" in data
        assert "researcher_system" in data
        assert "sysops_system" in data
        assert "classify" in data
        assert "planner" in data

    def test_load_prompt_missing_file(self):
        with pytest.raises(ConfigError):
            load_prompt("missing_file.json")

    def test_load_prompt_cached(self):
        path = Path("prompt.json")
        with patch("io.open", wraps=io.open) as mock_open:
            first = load_prompt(path)
            second = load_prompt(path)
        assert first is second
        mock_open.assert_called_once()
