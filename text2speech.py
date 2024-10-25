from openai import OpenAI

client = OpenAI()

def stream_audio_from_text(input, voice):
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice=voice,
        input=input,
    ) as response:
        response.stream_to_file("speech.mp3")