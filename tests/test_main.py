import unittest
from unittest.mock import patch
import requests

import main
from main import ask_llm, LLMServerUnavailable, check_command_error


class AskLLMTests(unittest.TestCase):
    @patch('requests.post')
    def test_connection_error_raises(self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError
        main.server_url = 'http://localhost'
        main.model = 'test-model'
        with self.assertRaises(LLMServerUnavailable):
            ask_llm('hi')


class CheckCommandErrorTests(unittest.TestCase):
    def test_case_insensitive(self):
        self.assertTrue(check_command_error('SyNtAx ErRoR somewhere'))


if __name__ == '__main__':
    unittest.main()
