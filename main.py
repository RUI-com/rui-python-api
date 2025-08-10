from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import subprocess
import tempfile
import os
import base64

app = FastAPI()

# Speech to Text Endpoint
@app.post("/stt")
async def stt(audio: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name

    result = subprocess.run(["python", "stt_script.py", tmp_path], capture_output=True, text=True)
    os.remove(tmp_path)

    return JSONResponse(content={"text": result.stdout.strip()})

# Text to Speech Endpoint
@app.post("/tts")
async def tts(text: str = Form(...)):
    out_path = "output.mp3"
    subprocess.run(["python", "gtts_script.py", "--text", text, "--out_path", out_path])
    
    with open(out_path, "rb") as f:
        audio_data = base64.b64encode(f.read()).decode()

    os.remove(out_path)
    return JSONResponse(content={"audio_base64": audio_data})
