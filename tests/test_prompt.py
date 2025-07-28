import unittest
from agent.prompt import load_prompt, ConfigError

class ConfigLoaderTest(unittest.TestCase):
    def test_load_prompt_success(self):
        data = load_prompt("prompt.json")
        self.assertIn("system", data)

    def test_load_prompt_missing_file(self):
        with self.assertRaises(ConfigError):
            load_prompt("missing_file.json")

if __name__ == "__main__":
    unittest.main()
