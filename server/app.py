import os
import tempfile
import torchaudio

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from faster_whisper import WhisperModel
from pydantic import BaseModel
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice

app = FastAPI()

# Initialize the TextToSpeech
tts = TextToSpeech()

model_size = "tiny.en"
model = WhisperModel(model_size, device="cuda", compute_type="float16")


@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...), save_path: str = Form(default=None)):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        contents = await file.read()
        temp_file.write(contents)
        temp_file_path = temp_file.name

    segments, info = model.transcribe(temp_file_path, beam_size=5)

    os.remove(temp_file_path)

    transcription = "\n".join([f"{segment.text}" for segment in segments])

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w') as f:
            f.write(transcription)

    response = {"transcription": transcription.split('\n')}
    return response

class SpeechRequest(BaseModel):
    text: str
    voice: str
    preset: str = "ultra-fast"

@app.post("/generate/")
async def generate_speech(request: SpeechRequest):
    """
    Generate speech from text using a specific voice and preset.
    """
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