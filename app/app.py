from agent import Agent
import gradio as gr
from text2speech import stream_audio_from_text
from gradio_toggle import Toggle
import json
from speech2text import speech2text

ag = Agent()

def load_state():
    chat_history = []
    tts_enabled = False
    activity = "Learning"
    level = "A1"
    select_voice = "alloy"
    topic = "Education"
    try:
        state = json.load(open('files/state.json'))
        chat_history = state['chat_history']
        tts_enabled = state['tts_enabled']
        activity = state['activity']
        level = state['level']
        select_voice = state['select_voice']
        topic = state['topic']
    except Exception as e:
        print("Something wrong!",e)
    return chat_history, tts_enabled, activity, level, select_voice, topic

def save_state(state):
    with open('files/state.json', 'w') as f:
        json.dump(state, f)
    
def chat(input, chat_history, tts_enabled, activity,level, select_voice,topic):
    inp = {
        "input": input,
        "chat_history": chat_history,
        "level": level,
        "topic": topic,
        "select_voice": select_voice,
        "tts_enabled": tts_enabled,
        "activity": activity
    }
    # if activity == "Reviewing":
    #     inp["reviewing_word"] = reviewing_word
    speech = None
    try:
        ag.switch_act(activity)
        response = ag.agent_executor.invoke(inp)
        # response = llm_invoke(inp, activity)
        chat_history.append({"role": "user", "content": input})
        chat_history.append({"role": "assistant", "content": str(response["output"])})
        if tts_enabled:
            speech = "files/audio/speech.mp3"
            stream_audio_from_text(str(response["output"]), select_voice, speech)
    except Exception as e:
        print(e)
    inp["chat_history"] = chat_history
    save_state(inp)
    return "", chat_history, speech

def get_pronounce(input, select_voice):
    try:
        speech = "files/audio/pronounce.mp3"
        stream_audio_from_text(input, select_voice, speech)
    except Exception as e:
        gr.Warning(f"Something wrong, try again! {e}")
    return speech,""
css ="""
#toggle {
    margin: 15px;
}

textarea {
    color:#00e0ff;
}
"""


def get_username(request: gr.Request):
    return request.username

with gr.Blocks(theme = gr.themes.Ocean(), css=css, title="Learn English with LLM") as demo:
   
    gr.Markdown("<h1 style='font-size: 30px'>Chat</h1>") 
    with gr.Row():
        with gr.Column(scale=2):       
            chatbot = gr.Chatbot(label="Chatbot",type='messages', autoscroll=True)  
            msg = gr.Textbox(container=False, interactive=True, elem_id="msg-textbox")
            with gr.Row():
                # with gr.Column():
                #     submit = gr.Button(value = "Submit")
                # with gr.Column():
                clear = gr.ClearButton([msg, chatbot])
            record_audio = gr.Audio(sources='microphone', type='filepath')
        with gr.Column(scale=1):
            activity = gr.Dropdown(['Learning','Reviewing'], label="Activity", interactive=True)
            level = gr.Dropdown(['A1','A2','B1','B2','C1','C2'], label="Level", interactive=True)
            topic = gr.Dropdown(['Education','Travel','Food and Cuisine','Technology','Health and Fitness','Environment','Arts and Culture','Sports','History','Current Events','Miscellaneous'], label="Topic", interactive=True)
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
                    select_voice = gr.Dropdown(['alloy','echo','fable','onyx','nova','shimmer'], label="Voice", interactive=True)
            pronounce_text  = gr.Textbox(interactive=True, label="Pronunciation", elem_id="pron-textbox")
            # pronounce_btn = gr.Button(value="Pronounce")
            pronounce_audio =  gr.Audio(label="Pronounce", type="filepath", autoplay=True)
            audio = gr.Audio(label="Text-to-Speech Response", type="filepath", autoplay=True, visible=False)
            # user_id = gr.Textbox(interactive=False, visible=False)
    # demo.load(get_username, inputs=None, outputs=user_id)
    demo.load(load_state,None, outputs=[chatbot,tts_toggle,activity,level,select_voice,topic])
    record_audio.stop_recording(speech2text, inputs=record_audio, outputs=[msg])
    msg.submit(chat, [msg, chatbot, tts_toggle, activity, level, select_voice, topic], [msg, chatbot, audio])
    pronounce_text.submit(get_pronounce, [pronounce_text,select_voice],[pronounce_audio,pronounce_text])



if __name__ == '__main__':
    demo.queue()
    demo.launch(favicon_path="files/images/icon.png")  # Chạy Gradio
