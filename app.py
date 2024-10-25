from re import S
from agent import Agent
import gradio as gr
from text2speech import stream_audio_from_text
from gradio_toggle import Toggle
from agent_tools import _load_random_vocabs
from speech2text import speech2text
import numpy as np
from pydub import AudioSegment

ag = Agent()

def chat(input, chat_history, tts_enabled,select_lang, select_voice):
    inp = {}
    inp["input"] = input
    inp["chat_history"] = chat_history[-5:]
    
    ag.switch_lang(select_lang)
    
    response = ag.agent_executor.invoke(inp)
    chat_history.append({"role": "user", "content": input})
    chat_history.append({"role": "assistant", "content": str(response["output"])})
    speech = None
    if tts_enabled:
        stream_audio_from_text(str(response["output"]), select_voice)
        speech = "speech.mp3"
    vocabs = _load_random_vocabs(rand = True)[0]
    return "", chat_history, speech, vocabs

css ="""
#toggle {
    margin: 15px;
}

textarea {
    color:#00e0ff;
}
"""
with gr.Blocks(theme = gr.themes.Ocean(), css=css) as demo:
    gr.Markdown("<h1 style='font-size: 30px'>Chat</h1>") 
    with gr.Row():
        with gr.Column(scale=2):       
            chatbot = gr.Chatbot(label="Chatbot",type='messages', autoscroll=True)  
            msg = gr.Textbox(container=False)
            record_audio = gr.Audio(sources='microphone', type='filepath')
            clear = gr.ClearButton([msg, chatbot])
        with gr.Column(scale=1):
            select_lang = gr.Dropdown(['English','Tiếng Việt'], label="Language", interactive=True)
            with gr.Row():
                with gr.Column(min_width=0):
                    tts_toggle = Toggle(
                        container= False,
                        info="Speak",
                        value=False,
                        color="green",
                        interactive=True,
                        elem_id="toggle",
                    )
                with gr.Column(min_width=250):
                    select_voice = gr.Dropdown(['alloy','echo','fable','onyx','nova','shrimmer'], label="Voice", interactive=True)
            audio = gr.Audio(label="Text-to-Speech Response", type="filepath", autoplay=True)
           
            vocabs_display = gr.Textbox(label="Vocabulary saved", max_lines=10, elem_id="vocabs")
    msg.submit(chat, [msg, chatbot, tts_toggle,select_lang, select_voice], [msg, chatbot, audio, vocabs_display])
    record_audio.stop_recording(speech2text, inputs=record_audio, outputs=[msg])
    
# Launch the app

if __name__ == "__main__":
    demo.launch()