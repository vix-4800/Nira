import re
from PyPDF2 import PdfReader

try:
    import whisper  # optional, used for transcribing audio
except Exception:  # pragma: no cover - whisper may be missing during tests
    whisper = None


def extract_text_from_pdf(path: str) -> str:
    """Return all text extracted from a PDF file located at ``path``."""
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
    return "\n".join(text).strip()


def summarize_text(text: str, sentences: int = 3) -> str:
    """Very simple summarization: return the first ``sentences`` sentences."""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(parts[:sentences]).strip()


def summarize_pdf(path: str, sentences: int = 3) -> str:
    """Extract text from a PDF and return a short summary."""
    text = extract_text_from_pdf(path)
    return summarize_text(text, sentences)


def count_words_in_file(path: str) -> str:
    """Return the number of words in a text file."""
    with open(path, "r", encoding="utf-8") as fh:
        words = fh.read().split()
    return str(len(words))


def transcribe_audio(path: str, model_name: str = "base") -> str:
    """Transcribe an audio file using OpenAI Whisper if available."""
    if whisper is None:
        raise RuntimeError("whisper package not installed")
    model = whisper.load_model(model_name)
    result = model.transcribe(path)
    return result.get("text", "").strip()
