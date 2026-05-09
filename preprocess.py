import os
import subprocess
import librosa
import soundfile as sf
import noisereduce as nr
import numpy as np
import sys
import shutil

#Creating folders for audio and the  15 second segments of the audio 
#yt_dlp is used to extract and download raw audio
os.makedirs("raw_audio", exist_ok=True)
os.makedirs("clean_segments", exist_ok=True)

def download_audio(url, output_folder="raw_audio"):
    command = [
        sys.executable, "-m","yt_dlp",
        "-x",
        "--audio-format", "wav",

        "--audio-quality", "0",
        "--ffmpeg-location", ".",

        "-o", f"{output_folder}/%(title)s.%(ext)s",
        url
    ]
    subprocess.run(command, check=True)
    print("Download complete.")

# download_audio("https://youtu.be/SvHrpyhZtBc?si=m0MyxYfLJbnNfvJK")

#processing the 42 min audio file and splitting them in 10 second segments
#mono means single audio
#the for loop of splitting the segments uses slice operator
#the for loop for saving used idx03d format to name the files and they're all being saved to the clean_segments file 
def audio_processing(file_path):
        print("load audio")
        audio, sample_rate = librosa.load(file_path, sr=22050, mono= True)

        print("reduce noise")
        reduced = nr.reduce_noise (y=audio,sr= sample_rate)

        print("split to segments")
        segment_length = sample_rate*10
        segments =  [reduced[i:i+segment_length]
           for i in range(0, len(reduced), segment_length)]
    
        print(f"saving {len(segments)} in the file")
        for idx, segments in enumerate(segments):
            output_path = f"clean_segments/segments {idx:03d}.wav"
            sf.write(output_path,segments,sample_rate)

audio_processing("raw_audio/output.wav")

#We're using only top 10 audio files from the clean_segments folder, these top 10 are decided by the RMS


def filter_segments(folder = "clean_segments",min_duration = 5.0):
    good_segments = []


    for filename in os.listdir(folder):
          if filename.endswith(".wav"):
            path = os.path.join(folder,filename)
            audio,sr = librosa.load(path,sr = 22050)
            duration = librosa.get_duration(y=audio, sr=sr )
            rms = float(np.sqrt(np.mean(audio**2)))
            
            if duration >= min_duration and rms >= 0.01:
               good_segments.append((filename,duration,rms))
          

    good_segments.sort(key = lambda x:x[2], reverse = True)

      
    print(f"Found {len(good_segments)} good segments")
    for name, dur, rms in good_segments[:10]:
        print(f"{name} | {dur:.1f}s | energy: {rms:.4f}")
    return good_segments  
filter_segments()





def save_best_segments(best_segments,source_folder = "clean_segments", dest_folder = "reference_audio"):
     os.makedirs(dest_folder,exist_ok=True)
     for filename,duration,rms in best_segments[:10]:
        src = os.path.join(source_folder, filename)
        dst = os.path.join(dest_folder, filename)
        shutil.copy(src, dst)
        print(f"Saved {filename}")




best = filter_segments()
save_best_segments(best)