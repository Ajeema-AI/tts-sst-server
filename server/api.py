from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import torch
import torchaudio
import os

from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice, load_voices

app = FastAPI()

# Initialize the TextToSpeech
tts = TextToSpeech()

class SpeechRequest(BaseModel):
    text: str
    voice: str
    preset: str = "fast"

@app.post("/generate/")
async def generate_speech(request: SpeechRequest):
    """
    Generate speech from text using a specific voice and preset.
    """
    # Access fields from the request using request.<fieldname>
    text = request.text
    voice = request.voice
    preset = request.preset

    if voice not in ['random', 'custom'] and not os.path.exists(f'tortoise/voices/{voice}'):
        raise HTTPException(status_code=404, detail="Voice not found")

    if voice == 'random':
        voice_samples, conditioning_latents = None, None
    else:
        voice_samples, conditioning_latents = load_voice(voice)

    gen = tts.tts_with_preset(text, voice_samples=voice_samples, conditioning_latents=conditioning_latents, preset=preset)
    filename = f"generated_{voice}.wav"
    torchaudio.save(filename, gen.squeeze(0).cpu(), 24000)
    return FileResponse(filename)

@app.post("/upload_voice/")
async def upload_voice(voice_name: str, files: List[UploadFile] = File(...)):
    """
    Upload custom voice samples.
    """
    custom_voice_folder = f"tortoise/voices/{voice_name}"
    os.makedirs(custom_voice_folder, exist_ok=True)

    for i, file in enumerate(files):
        contents = await file.read()
        with open(os.path.join(custom_voice_folder, f'{i}.wav'), 'wb') as f:
            f.write(contents)

    return {"message": "Voice uploaded successfully", "voice_name": voice_name}
