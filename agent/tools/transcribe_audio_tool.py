from pydantic import BaseModel, Field
from langchain_core.tools import tool

from .file_tools import transcribe_audio

class TranscribeAudioInput(BaseModel):
    path: str = Field(..., description="Path to the audio file")
    model_name: str = Field(default="base", description="Whisper model name")

@tool("TranscribeAudio", args_schema=TranscribeAudioInput)
def transcribe_audio_tool(path: str, model_name: str = "base") -> str:
    """Transcribe speech from an audio file using Whisper if available."""
    return transcribe_audio(path, model_name=model_name)
