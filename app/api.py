
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.responses import FileResponse
import init
from text2speech import stream_audio_from_text

class Config(BaseModel):
    activity: str = "Learning"
    level: str = "B2"
    topic: str = "Education"
    userMessage: str = ""
    chatHistory: list = []
class Audio(BaseModel):
    text : str = ""
    voice: str = "alloy"
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)