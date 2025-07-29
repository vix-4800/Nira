from pathlib import Path
from .pdf_tools import summarize_text
from ..env import get_obsidian_vault


def _vault_path() -> Path:
    vault = get_obsidian_vault()
    if not vault:
        raise RuntimeError("OBSIDIAN_VAULT not configured")
    return Path(vault)


def create_note(title: str, content: str = "") -> str:
    """Create a new markdown note in the Obsidian vault."""
    path = _vault_path() / f"{title}.md"
    if path.exists():
        return f"Note already exists: {path}"
    try:
        path.write_text(content, encoding="utf-8")
        return f"Created {path}"
    except Exception as e:
        return f"Failed to create note: {e}"


def summarize_note(title: str, sentences: int = 3) -> str:
    """Return a short summary of the specified note."""
    path = _vault_path() / f"{title}.md"
    if not path.is_file():
        return f"(File not found: {path})"
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Failed to read note: {e}"
    return summarize_text(text, sentences)
