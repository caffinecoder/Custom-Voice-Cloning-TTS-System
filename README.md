# Telugu Voice Cloning System

An end-to-end Telugu voice cloning pipeline that clones a target speaker's voice from reference audio and generates natural-sounding Telugu speech from text input.

Built using [AI4Bharat's IndicF5](https://huggingface.co/ai4bharat/IndicF5) — a 0.4B parameter multilingual TTS model trained on 1417 hours of high-quality Indian language speech.

---

## Demo

> Upload a short Telugu audio clip → paste Telugu text → get output in the speaker's voice.

*(HuggingFace Spaces deployment coming soon)*

---

## Features

- Automated audio sourcing from YouTube using `yt-dlp`
- Audio preprocessing pipeline: noise reduction, resampling, segmentation
- RMS-based energy filtering to select optimal reference audio segments
- Voice cloning inference using IndicF5 on CUDA GPU
- Supports Telugu text input with natural prosody and speaker characteristics

---

## Project Structure

```
voice-clone/
├── preprocess.py        # Full audio preprocessing pipeline
├── raw_audio/           # Downloaded source audio (gitignored)
├── clean_segments/      # Segmented audio clips (gitignored)
├── reference_audio/     # Top 10 reference clips selected by RMS (gitignored)
└── README.md
```

---

## Pipeline Overview

```
YouTube Video
      ↓
  yt-dlp (download audio)
      ↓
  ffmpeg (convert to WAV, 22050Hz mono)
      ↓
  librosa + noisereduce (clean audio)
      ↓
  Split into 10-second segments (289 total)
      ↓
  RMS energy filtering (top 10 selected)
      ↓
  IndicF5 inference (voice cloning)
      ↓
  Output WAV in target speaker's voice
```

---

## Setup

### Prerequisites
- Python 3.10
- CUDA-compatible GPU (recommended)
- FFmpeg installed and accessible in PATH

### Installation

```bash
git clone https://github.com/caffinecoder/Custom-Voice-Cloning-TTS-System.git
cd Custom-Voice-Cloning-TTS-System
pip install git+https://github.com/ai4bharat/IndicF5.git
pip install transformers==4.49.0 librosa soundfile noisereduce yt-dlp numpy
```

### Preprocessing

```bash
python preprocess.py
```

This will:
1. Download audio from the configured YouTube URL
2. Clean and segment the audio
3. Select the top 10 reference clips by RMS energy
4. Save them to `reference_audio/`

### Inference (Google Colab recommended)

```python
from transformers import AutoModel
import numpy as np
import soundfile as sf

model = AutoModel.from_pretrained("ai4bharat/IndicF5", trust_remote_code=True)

audio = model(
    "మీరు టైప్ చేసిన తెలుగు వాక్యం ఇక్కడ పెట్టండి.",
    ref_audio_path="reference_audio/segments_184.wav",
    ref_text=""
)

if audio.dtype == np.int16:
    audio = audio.astype(np.float32) / 32768.0

sf.write("output.wav", np.array(audio, dtype=np.float32), samplerate=24000)
```

---

## Ethics & Consent

This project was built with explicit consent from the voice donor.

- Voice cloning is performed only on audio for which the developer has permission
- No voice data is stored or shared beyond local use
- Users of this system are responsible for obtaining consent before cloning any voice
- Unauthorized voice cloning is strictly prohibited per IndicF5's Terms of Use

---

## Known Issues & Solutions

**`transformers==5.0` meta tensor error**
IndicF5 is incompatible with transformers 5.0+ due to a meta tensor initialization conflict. Downgrade to `transformers==4.49.0` to resolve.

**Slow inference on CPU**
IndicF5 requires a GPU for reasonable inference speed. Use Google Colab with a T4 GPU runtime for best results.

---

## Tech Stack

- **Model:** AI4Bharat IndicF5 (F5-TTS based)
- **Audio processing:** librosa, noisereduce, soundfile, pydub
- **Download:** yt-dlp, ffmpeg
- **Inference:** PyTorch, HuggingFace Transformers
- **Language:** Telugu (తెలుగు)

---

## Acknowledgements

- [AI4Bharat](https://ai4bharat.iitm.ac.in/) for IndicF5
- [F5-TTS](https://github.com/SWivid/F5-TTS) which IndicF5 is based on
- [Coqui TTS](https://github.com/coqui-ai/TTS) for inspiration

---

## Citation

```bibtex
@misc{AI4Bharat_IndicF5_2025,
  author = {Praveen S V and Srija Anand and Soma Siddhartha and Mitesh M. Khapra},
  title  = {IndicF5: High-Quality Text-to-Speech for Indian Languages},
  year   = {2025},
  url    = {https://github.com/AI4Bharat/IndicF5}
}
```
