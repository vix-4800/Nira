import unittest
from unittest.mock import patch
import requests

from main import ask_llm, LLMServerUnavailable


class AskLLMTests(unittest.TestCase):
    @patch('requests.post')
    def test_connection_error_raises(self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError
        with self.assertRaises(LLMServerUnavailable):
            ask_llm('hi', 'http://localhost', 'model')


if __name__ == '__main__':
    unittest.main()
