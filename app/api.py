
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.responses import FileResponse
from speech2text import speech2text
import agent_tools
import init

from text2speech import stream_audio_from_text
import speech_recognition as sr
class Config(BaseModel):
    activity: str = "Learning"
    level: str = "B2"
    topic: str = "Education"
    userMessage: str = ""
    chatHistory: list = []
class Audio(BaseModel):
    text : str = ""
    voice: str = "alloy"
    
class Vocab(BaseModel):
    vocab : str = ""
    topic: str = ""
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/api/response")
async def response(config: Config):
    try:
        text = init.chat(config.userMessage, config.chatHistory, config.activity, config.level, config.topic).replace("```","").replace("html","")
        return JSONResponse(
            content={"text": text},
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500  # Trả về mã lỗi 500 nếu có vấn đề
        )


@app.get("/api/audio/{audio_filename:path}")
async def get_audio(audio_filename: str):
    return FileResponse(audio_filename, media_type="audio/mpeg")

@app.post("/api/audio")
async def post_audio(audio: Audio):  
    audio_filename = stream_audio_from_text(audio.text,audio.voice, "files/audio/speech.mp3")
    return JSONResponse(
            content={"audio": audio_filename},
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

@app.post("/api/save_vocab")
async def save_vocabs(vocab :Vocab):
    try:
        v = vocab.vocab
        t = vocab.topic.lower()
        if not agent_tools._check_vocab_exists(t, v):
            agent_tools._save_vocab(t, v)
            return JSONResponse(
                content={"message": "Vocabs saved successfully!"},
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        else:
            return JSONResponse(
                content={"message": "Vocab already exists!"},
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500  # Trả về mã lỗi 500 nếu có vấn đề
        )
    
TEMP_DIR = "files/audio"

@app.post("/api/speech_to_text")
async def speech_to_text(audio: UploadFile = File(...)):
    # print(audio)
    try:
        file_path = os.path.join(TEMP_DIR, audio.filename)
        with open(file_path, "wb") as f:
            f.write(await audio.read())
        # Chuyển đổi âm thanh sang văn bản
        text =  speech2text(file_path)
        os.remove(file_path)

        return {"text": text}
        
    except sr.UnknownValueError:
        raise JSONResponse(status_code=400, content="Could not understand audio.")
    except sr.RequestError as e:
        raise JSONResponse(status_code=500, content=f"Error with the speech recognition service: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)