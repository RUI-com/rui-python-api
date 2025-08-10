from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import subprocess
import tempfile
import os
import base64

app = FastAPI()

# هنا بتحط إعدادات CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # ممكن تحط هنا دومين الfrontend بدل "*"
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
@app.get("/")
def health_check():
    return {"status": "ok"}
# Speech to Text Endpoint
@app.post("/stt")
async def stt(audio: UploadFile = File(...)):
    if audio.content_type not in ["audio/webm", "audio/mpeg", "audio/wav"]:
        return JSONResponse(content={"error": "Unsupported audio format"}, status_code=400)

    contents = await audio.read()
    if len(contents) == 0:
        return JSONResponse(content={"error": "Empty audio file"}, status_code=400)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        script_path = os.path.join(os.path.dirname(__file__), "stt_script.py")
        result = subprocess.run(["python", script_path, tmp_path], capture_output=True, text=True, encoding="utf-8")
        if result.returncode != 0:
            return JSONResponse(content={"error": f"STT script error: {result.stderr}"}, status_code=500)
        return JSONResponse(content={"text": result.stdout.strip()})
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

# Text to Speech Endpoint
@app.post("/tts")
async def tts(text: str = Form(...)):
    out_path = "output.mp3"
    script_path = os.path.join(os.path.dirname(__file__), "gtts_script.py")
    subprocess.run(["python", script_path, "--text", text, "--out_path", out_path])

    with open(out_path, "rb") as f:
        audio_data = base64.b64encode(f.read()).decode()

    os.remove(out_path)
    return JSONResponse(content={"audio_base64": audio_data})
