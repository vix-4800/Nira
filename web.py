from typing import Optional

import gradio as gr

from agent.agents.planner_executor import PlannerExecutor

try:
    from agent.core.voice_recognizer import transcribe_whisper
    from agent.core.voice_synthesizer import VoiceSynthesizer

    pass
except Exception:  # pragma: no cover - executed only when missing
    transcribe_whisper = None  # type: ignore
    VoiceSynthesizer = None  # type: ignore
    pass

voice_modules_available = (
    transcribe_whisper is not None and VoiceSynthesizer is not None
)

voice_synthesizer: Optional["VoiceSynthesizer"] = None

planner = PlannerExecutor()


def chat(user_message: str, history: list[dict[str, str]], speak: bool):
    history = history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": ""},
    ]
    response = planner.run(user_message)
    history[-1]["content"] = response

    if speak and voice_modules_available:
        global voice_synthesizer
        if voice_synthesizer is None and VoiceSynthesizer is not None:
            voice_synthesizer = VoiceSynthesizer()
        if voice_synthesizer is not None:
            voice_synthesizer.speak(response)

    return "", history


def voice_to_text() -> str:
    if transcribe_whisper is None:
        return ""
    return transcribe_whisper()


def main() -> None:
    with gr.Blocks() as demo:
        gr.Markdown("# Nira Chat")
        chatbot = gr.Chatbot(type="messages")
        with gr.Row():
            msg = gr.Textbox(label="Message", scale=4)
            submit = gr.Button("Submit", scale=1)
            voice_btn = gr.Button("Voice", scale=1)
        with gr.Row():
            speak_toggle = gr.Checkbox(False, label="Speak")
            clear = gr.Button("Clear")

        submit.click(chat, [msg, chatbot, speak_toggle], [msg, chatbot])
        msg.submit(chat, [msg, chatbot, speak_toggle], [msg, chatbot])
        voice_btn.click(voice_to_text, None, msg)
        clear.click(lambda: [], None, chatbot, queue=False)

    demo.launch()


if __name__ == "__main__":
    main()
