from openai import OpenAI
import re
client = OpenAI()

def stream_audio_from_text(input, voice, output = "speech.mp3"):
    
    r =re.compile(r'<.*?>')
    input = r.sub('',input)
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice=voice,
        input=input,
    ) as response:
        response.stream_to_file(output)
    
    return output