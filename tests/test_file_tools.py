import unittest
from unittest import mock

from agent.tools.transcribe_audio_tool import transcribe_audio_tool


class FileToolsTest(unittest.TestCase):

    @mock.patch("importlib.import_module")
    def test_transcribe_audio_missing_whisper(self, mock_import):
        mock_whisper = mock.Mock()
        mock_whisper.load_model.return_value.transcribe.return_value = {"text": "hi"}
        mock_import.return_value = mock_whisper
        # Ensure cache is clear
        transcribe_audio_tool.func.whisper = None
        transcribe_audio_tool.func.whisper_model = None
        result = transcribe_audio_tool.func("file.wav", model_name="base")
        self.assertEqual(result, "hi")


if __name__ == "__main__":
    unittest.main()
