from langchain.agents import Tool
from .bash_tool import run_bash_command
from .file_tools import (
    extract_text_from_pdf,
    summarize_pdf,
    count_words_in_file,
    transcribe_audio,
)

tools = [
    Tool(
        name="RunBashCommand",
        func=run_bash_command,
        description="Executes a system bash command and returns the result. Use it for file searching, system management, and other terminal tasks.",
    ),
    Tool(
        name="ExtractTextFromPDF",
        func=extract_text_from_pdf,
        description="Extract the textual contents from a PDF file given its path.",
    ),
    Tool(
        name="SummarizePDF",
        func=summarize_pdf,
        description="Provide a short summary of a PDF document.",
    ),
    Tool(
        name="CountWordsInFile",
        func=count_words_in_file,
        description="Return the number of words in a text file.",
    ),
    Tool(
        name="TranscribeAudio",
        func=transcribe_audio,
        description="Transcribe speech from an audio file using Whisper if available.",
    ),
]
