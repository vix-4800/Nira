from .bash_tool import run_bash_command
from .telegram_tool import send_telegram_message
from .file_tools import (
    extract_text_from_pdf,
    summarize_pdf,
    count_words_in_file,
    transcribe_audio,
)

tools = [
    run_bash_command,
    extract_text_from_pdf,
    summarize_pdf,
    count_words_in_file,
    transcribe_audio,
    send_telegram_message,
]

