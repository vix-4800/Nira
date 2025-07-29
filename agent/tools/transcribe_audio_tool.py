import importlib

from langchain_core.tools import tool
from pydantic import BaseModel, Field

whisper = None


class TranscribeAudioInput(BaseModel):
    path: str = Field(..., description="Path to the audio file")
    model_name: str = Field(default="base", description="Whisper model name")


@tool("TranscribeAudio", args_schema=TranscribeAudioInput)
def transcribe_audio_tool(path: str, model_name: str = "base") -> str:
    """Transcribe speech from an audio file using Whisper if available."""
    global whisper
    if whisper is None:
        try:
            whisper = importlib.import_module("whisper")
        except Exception:
            raise RuntimeError("whisper package not installed")
    model = whisper.load_model(model_name)
    result = model.transcribe(path)
    return result.get("text", "").strip()
