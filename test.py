import gradio as gr

def create_greeting(request: gr.Request):
    return request.username

with gr.Blocks() as demo:
    user_ip = gr.Markdown(value="Not logged in")

    demo.load(create_greeting, inputs=None, outputs=user_ip)

demo.launch(auth=("admin", "admin"))