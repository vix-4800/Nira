import pytest

from agent.core.prompt import ConfigError, load_prompt


class TestConfigLoader:
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
