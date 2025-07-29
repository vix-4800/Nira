from pydantic import BaseModel, Field
from langchain_core.tools import tool

try:
    import whisper
except Exception:
    whisper = None


def transcribe_audio(path: str, model_name: str = "base") -> str:
    """Transcribe an audio file using OpenAI Whisper if available."""
    if whisper is None:
        raise RuntimeError("whisper package not installed")
    model = whisper.load_model(model_name)
    result = model.transcribe(path)
    return result.get("text", "").strip()

class TranscribeAudioInput(BaseModel):
    path: str = Field(..., description="Path to the audio file")
    model_name: str = Field(default="base", description="Whisper model name")

@tool("TranscribeAudio", args_schema=TranscribeAudioInput)
def transcribe_audio_tool(path: str, model_name: str = "base") -> str:
    """Transcribe speech from an audio file using Whisper if available."""
    return transcribe_audio(path, model_name=model_name)
