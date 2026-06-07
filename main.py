from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import numpy as np
import soundfile as sf
import shutil
import uuid
import os

# NOTE: The `model` variable is loaded externally at runtime.
# When running locally or on a server, load the model before starting the app:
#   from transformers import AutoModel
#   model = AutoModel.from_pretrained("ai4bharat/IndicF5", trust_remote_code=True)
# When running in Colab, the model is loaded in the notebook and passed into scope.
# See voice_clone.ipynb for the full inference setup.

app = FastAPI(title="Telugu Voice Cloning")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/clone-voice")
async def clone_voice(
    audio: UploadFile = File(...),
    text: str = Form(...),
    language: str = Form(default="te"),
    consent: bool = Form(...)
):
    if not consent:
        raise HTTPException(status_code=400, detail="Consent is required to use this service.")

    if not text.strip():
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")

    # Use unique filenames per request to avoid conflicts when handling concurrent users
    rid = uuid.uuid4().hex
    input_path = f"/tmp/{rid}_input.wav"
    output_path = f"/tmp/{rid}_output.wav"

    try:
        # Save uploaded reference audio to disk
        with open(input_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)

        # Run voice cloning inference
        # `model` must be loaded and available in scope before the server starts
        audio_output = model(
            text,
            ref_audio_path=input_path,
            ref_text=""
        )

        # IndicF5 may return int16 audio — convert to float32 for soundfile
        if audio_output.dtype == np.int16:
            audio_output = audio_output.astype(np.float32) / 32768.0

        sf.write(output_path, np.array(audio_output, dtype=np.float32), samplerate=24000)

        return FileResponse(output_path, media_type="audio/wav", filename="cloned_voice.wav")

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up input file after request completes
        if os.path.exists(input_path):
            os.remove(input_path)