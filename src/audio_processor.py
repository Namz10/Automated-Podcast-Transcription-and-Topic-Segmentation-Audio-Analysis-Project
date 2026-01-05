import librosa
import soundfile as sf
import numpy as np
import os

def preprocess_audio(input_path, output_path):
    print(f"Preprocessing audio: {input_path}")
    # Load audio at 16kHz mono (Whisper requirement)
    y, sr = librosa.load(input_path, sr=16000, mono=True)
    
    # Normalization
    y_norm = librosa.util.normalize(y)
    
    # Simple silence trimming
    y_trimmed, _ = librosa.effects.trim(y_norm, top_db=20)
    
    # Save processed audio
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, y_trimmed, sr)
    print(f"Processed audio saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    preprocess_audio("data/raw/audio/episode_sample.wav", "data/processed/episode_sample_cleaned.wav")
