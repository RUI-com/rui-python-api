from fastapi import FastAPI, File, UploadFile
import subprocess
import tempfile
import os

app = FastAPI()

@app.post("/stt")
async def stt(audio: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name

    result = subprocess.run(["python", "stt_script.py", tmp_path], capture_output=True, text=True)
    os.remove(tmp_path)
    return {"text": result.stdout.strip()}

@app.post("/tts")
async def tts(text: str):
    out_path = "output.mp3"
    subprocess.run(["python", "gtts-script.py", "--text", text, "--out_path", out_path])
    with open(out_path, "rb") as f:
        audio_data = f.read()
    os.remove(out_path)
    return {"audio_base64": audio_data.encode("base64").decode()}
