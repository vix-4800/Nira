import gradio as gr

from agent.agents.planner_executor import PlannerExecutor

try:
    from agent.core.voice_recognizer import transcribe_whisper
    from agent.core.voice_synthesizer import VoiceSynthesizer

    voice_modules_available = True
except Exception:  # pragma: no cover - executed only when missing
    transcribe_whisper = None
    VoiceSynthesizer = None
    voice_modules_available = False

voice_synthesizer = None

planner = PlannerExecutor()


def chat(user_message: str, history: list[tuple[str, str]], speak: bool):
    response = planner.run(user_message)
    history = history + [(user_message, response)]
    if speak and voice_modules_available:
        global voice_synthesizer
        if voice_synthesizer is None:
            voice_synthesizer = VoiceSynthesizer()
        voice_synthesizer.speak(response)
    return "", history


def voice_to_text() -> str:
    if transcribe_whisper is None:
        return ""
    return transcribe_whisper()


with gr.Blocks() as demo:
    gr.Markdown("# Nira Chat")
    chatbot = gr.Chatbot()
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
