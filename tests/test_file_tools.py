from unittest import mock


from agent.core import whisper_utils
from agent.tools.transcribe_audio_tool import transcribe_audio_tool


class TestFileTools:

    @mock.patch("importlib.import_module")
    def test_transcribe_audio_missing_whisper(self, mock_import):
        mock_whisper = mock.Mock()
        mock_whisper.load_model.return_value.transcribe.return_value = {"text": "hi"}
        mock_import.return_value = mock_whisper
        # Ensure cache is clear
        whisper_utils.whisper = None
        whisper_utils._models.clear()
        result = transcribe_audio_tool.func("file.wav", model_name="base")
        assert result == "hi"
