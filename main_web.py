import gradio as gr

from agent.agents.planner_executor import PlannerExecutor

planner = PlannerExecutor()


def chat(user_message: str, history: list[tuple[str, str]]):
    response = planner.run(user_message)
    history = history + [(user_message, response)]
    return "", history


with gr.Blocks() as demo:
    gr.Markdown("# Nira Chat")
    chatbot = gr.Chatbot()
    with gr.Row():
        msg = gr.Textbox(label="Message", scale=4)
        submit = gr.Button("Submit", scale=1)
    clear = gr.Button("Clear")

    submit.click(chat, [msg, chatbot], [msg, chatbot])
    msg.submit(chat, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: [], None, chatbot, queue=False)


demo.launch()
