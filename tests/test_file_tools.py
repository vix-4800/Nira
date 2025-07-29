import sys
import unittest
from pathlib import Path
from unittest import mock
from agent.tools.file_tools import transcribe_audio

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

class FileToolsTest(unittest.TestCase):

    @mock.patch('agent.tools.file_tools.whisper')
    def test_transcribe_audio_missing_whisper(self, mock_whisper):
        mock_whisper.load_model.return_value.transcribe.return_value = {'text': 'hi'}
        result = transcribe_audio('file.wav', model_name='base')
        self.assertEqual(result, 'hi')


if __name__ == '__main__':
    unittest.main()
