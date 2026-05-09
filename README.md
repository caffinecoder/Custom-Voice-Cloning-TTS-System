Custom Voice Cloning TTS System

A Python-based Text-to-Speech (TTS) application that replicates human voices from sample audio using APIs. Designed for accessibility and creative applications.

 Features
 
- Clone a custom voice from uploaded audio
- Generate speech from user input text
- Web interface using Flask
- API integration (e.g., ElevenLabs)

Tech Stack

- Python
- Flask
- ElevenLabs API (or other TTS)
- HTML/CSS (for front-end if any)

 How It Works
 
1. Upload a short voice sample
2. Enter text
3. TTS engine clones the voice and generates audio
4. Output is returned as a downloadable or streamable file

Installation

```bash
git clone https://github.com/your-username/tts-voice-cloning
cd tts-voice-cloning
pip install -r requirements.txt
python app.py
