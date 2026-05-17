from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import numpy as np
import soundfile as sf
import shutil
import os





app = FastAPI(title= "telugu voice cloning")


@app.get("/health")
def health_check():
    return{"status":"ok"}

@app.post("/clone-voice")
async def clone_voice(     
    audio: UploadFile = File(...),
    text: str = Form(...),
    language: str = Form (default = "te"),
    consent: bool  = Form(...)  
):
 try:
    if not consent: 
        raise HTTPException(status_code= 400, detail="consent")
    
    if not text.strip():
        raise HTTPException(status_code = 400, detail="feild cannot be empty")
    

    input_path = f"temp_input.wav"
    with open(input_path, "wb") as f: 
            shutil.copyfileobj(audio.file, f)

    
    # Generate cloned audio
    output_path = "temp_output.wav"
    audio_output = model(
        text,
        ref_audio_path=input_path,
        ref_text=""
    )
    
    if audio_output.dtype == np.int16:
        audio_output = audio_output.astype(np.float32) / 32768.0
    
    sf.write(output_path, np.array(audio_output, dtype=np.float32), samplerate=24000)
    
    return FileResponse(output_path, media_type="audio/wav", filename="cloned_voice.wav")
 
 except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))