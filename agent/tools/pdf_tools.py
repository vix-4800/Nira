import re
from PyPDF2 import PdfReader
import os

MAX_PAGES = 30
MAX_CHARS = 30_000


def summarize_text(text: str, sentences: int = 3) -> str:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(parts[:sentences]).strip()


def summarize_pdf(path: str, sentences: int = 3) -> str:
    text = extract_text_from_pdf(path)
    if text.startswith("(File not found"):
        return text
    return summarize_text(text, sentences)


def count_words_in_file(path: str) -> str:
    """Return the number of words in a text file."""
    with open(path, "r", encoding="utf-8") as fh:
        words = fh.read().split()
    return str(len(words))


def extract_text_from_pdf(path: str, max_pages: int = MAX_PAGES) -> str:
    if not os.path.isfile(path):
        return f"(File not found: {path})"
    reader = PdfReader(path)
    pages = reader.pages[:max_pages]
    text = []
    for p in pages:
        page_text = p.extract_text() or ""
        text.append(page_text)
    joined = "\n".join(text).strip()
    return joined[:MAX_CHARS]
