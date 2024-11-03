from openai import OpenAI
from llm_model import llm_openai
from prompts import prompt_format
client = OpenAI()

def stream_audio_from_text(input, voice, output = "speech.mp3"):
    
    chain = prompt_format | llm_openai
    input = chain.invoke({"html":input}).content
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice=voice,
        input=input,
    ) as response:
        response.stream_to_file(output)
    
    return output