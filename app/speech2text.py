from openai import OpenAI
client = OpenAI()

def speech2text(path):
    audio_file= open(path, "rb")
    translation = client.audio.translations.create(
    model="whisper-1", 
    file=audio_file
    )
    return translation.text