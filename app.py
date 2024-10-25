from agent import Agent
import gradio as gr
from text2speech import stream_audio_from_text
from gradio_toggle import Toggle
from agent_tools import _load_random_vocabs

ag = Agent()

def chat(input, chat_history, tts_enabled,select_lang):
    inp = {}
    inp["input"] = input
    inp["chat_history"] = chat_history
    
    ag.switch_lang(select_lang)
    
    response = ag.agent_executor.invoke(inp)
    chat_history.append({"role": "user", "content": input})
    chat_history.append({"role": "assistant", "content": str(response["output"])})
    speech = None
    if tts_enabled:
        stream_audio_from_text(str(response["output"]))
        speech = "speech.mp3"
    vocabs = _load_random_vocabs(rand = True)[0]
    return "", chat_history, speech, vocabs

css = """
#vocabs-display{font-size: 20px; font-color: #d400ff;}
"""

with gr.Blocks(theme=gr.themes.Ocean(), css=css) as demo:
    gr.Markdown("<h1 style='font-size: 50px'>Chat</h1>") 
    with gr.Row():
        with gr.Column(scale=2):       
            chatbot = gr.Chatbot(type="messages",autoscroll=True)
            msg = gr.Textbox()
            clear = gr.ClearButton([msg, chatbot])
        with gr.Column(scale=1):
            select_lang = gr.Dropdown(['English','Tiếng Việt'], label="Language", interactive=True)
                
            tts_toggle = Toggle(
                    container= False,
                    info="Text to Speech",
                    value=False,
                    color="green",
                    interactive=True,
                )
            audio = gr.Audio(label="Text-to-Speech Response", type="filepath", autoplay=True)
          
            vocabs_display = gr.Textbox(elem_id="vocabs-display",label="Vocabulary saved", max_lines=10, )
    msg.submit(chat, [msg, chatbot, tts_toggle,select_lang], [msg, chatbot, audio, vocabs_display])
# Launch the app

if __name__ == "__main__":
    demo.launch(share=True)