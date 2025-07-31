import unittest
from unittest.mock import patch

from agent.core.config import load_config


class ConfigTest(unittest.TestCase):
    def setUp(self):
        load_config.cache_clear()

    def test_defaults(self):
        with patch.dict("os.environ", {}, clear=True):
            cfg = load_config()
            self.assertEqual(cfg.server, "http://localhost:11434")
            self.assertEqual(cfg.model, "qwen3:4b")

    def test_auto_confirm_true(self):
        with patch.dict("os.environ", {"AUTO_CONFIRM": "yes"}):
            cfg = load_config()
            self.assertTrue(cfg.auto_confirm)

    def test_auto_confirm_false(self):
        with patch.dict("os.environ", {}, clear=True):
            cfg = load_config()
            self.assertFalse(cfg.auto_confirm)


if __name__ == "__main__":
    unittest.main()
