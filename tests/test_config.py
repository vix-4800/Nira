from unittest.mock import patch


from agent.core.config import load_config


class TestConfig:
    def setup_method(self):
        load_config.cache_clear()

    def test_defaults(self):
        with patch.dict("os.environ", {}, clear=True):
            cfg = load_config()
            assert cfg.server == "http://localhost:11434"
            assert cfg.model == "qwen3:4b"

    def test_auto_confirm_true(self):
        with patch.dict("os.environ", {"AUTO_CONFIRM": "yes"}):
            cfg = load_config()
            assert cfg.auto_confirm

    def test_auto_confirm_false(self):
        with patch.dict("os.environ", {}, clear=True):
            cfg = load_config()
            assert not cfg.auto_confirm
