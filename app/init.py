import json
from agent import Agent


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

def chat(input, chat_history, activity,level,topic):
    inp = {
        "input": input,
        "chat_history": chat_history,
        "level": level,
        "topic": topic
    }
    try:
        ag.switch_act(activity)
        response = ag.agent_executor.invoke(inp)
    except Exception as e:
        print(e)
    return str(response["output"])