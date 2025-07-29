import os
import glob
from typing import List

try:
    import whisper
except Exception:
    whisper = None

def find_file(pattern: str, root: str = ".") -> List[str]:
    """
    Recursively search for files matching the pattern under 'root'
    and return a list of absolute paths.
    Example pattern: "*.pdf" or "report_2024.pdf"
    """
    matches = glob.glob(os.path.join(root, "**", pattern), recursive=True)
    return [os.path.abspath(p) for p in matches]

def transcribe_audio(path: str, model_name: str = "base") -> str:
    """Transcribe an audio file using OpenAI Whisper if available."""
    if whisper is None:
        raise RuntimeError("whisper package not installed")
    model = whisper.load_model(model_name)
    result = model.transcribe(path)
    return result.get("text", "").strip()
