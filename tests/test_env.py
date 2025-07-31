import unittest
from unittest.mock import patch

from agent import env


class EnvGetterTest(unittest.TestCase):
    def test_get_server_default(self):
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(env.get_server("http://local"), "http://local")

    def test_get_auto_confirm_true(self):
        with patch.dict("os.environ", {"AUTO_CONFIRM": "yes"}):
            self.assertTrue(env.get_auto_confirm())

    def test_get_auto_confirm_false(self):
        with patch.dict("os.environ", {}, clear=True):
            self.assertFalse(env.get_auto_confirm())


if __name__ == "__main__":
    unittest.main()
