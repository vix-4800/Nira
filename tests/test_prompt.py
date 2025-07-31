import unittest

from agent.core.prompt import ConfigError, load_prompt


class ConfigLoaderTest(unittest.TestCase):
    def test_load_prompt_success(self):
        data = load_prompt("prompt.json")
        self.assertIn("system", data)
        self.assertIn("coder_system", data)
        self.assertIn("researcher_system", data)
        self.assertIn("sysops_system", data)
        self.assertIn("classify", data)
        self.assertIn("planner", data)

    def test_load_prompt_missing_file(self):
        with self.assertRaises(ConfigError):
            load_prompt("missing_file.json")


if __name__ == "__main__":
    unittest.main()
