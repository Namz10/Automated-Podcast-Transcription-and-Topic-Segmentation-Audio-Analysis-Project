import librosa
import soundfile as sf
import numpy as np
import os
import noisereduce as nr
from pydub import AudioSegment

def preprocess_audio(input_path, output_dir, audio_id):
    """
    Preprocesses a single audio file:
    1. Resample to 16kHz
    2. Mono conversion
    3. Noise reduction
    4. Normalization
    5. Chunking into 20-30s segments
    """
    print(f"Preprocessing audio: {input_path}")
    
    try:
        # Load audio at 16kHz mono
        # Librosa load returns y (audio array) and sr (sample rate)
        y, sr = librosa.load(input_path, sr=16000, mono=True)
        
        # Noise reduction
        print("Applying noise reduction...")
        y_denoised = nr.reduce_noise(y=y, sr=sr)
        
        # Normalization (Root Mean Square normalization)
        print("Applying normalization...")
        y_norm = librosa.util.normalize(y_denoised)
        
        # Silence trimming
        y_trimmed, _ = librosa.effects.trim(y_norm, top_db=25)
        
        # Chunking: 20-30 seconds
        chunk_length_s = 25
        chunk_samples = chunk_length_s * sr
        
        total_samples = len(y_trimmed)
        num_chunks = int(np.ceil(total_samples / chunk_samples))
        
        chunk_dir = os.path.join(output_dir, str(audio_id))
        os.makedirs(chunk_dir, exist_ok=True)
        
        chunk_info = []
        
        for i in range(num_chunks):
            start_sample = i * chunk_samples
            end_sample = min((i + 1) * chunk_samples, total_samples)
            
            chunk = y_trimmed[start_sample:end_sample]
            
            chunk_file = os.path.join(chunk_dir, f"chunk_{i}.wav")
            sf.write(chunk_file, chunk, sr)
            
            chunk_info.append({
                "audio_id": audio_id,
                "chunk_id": i,
                "file_path": chunk_file,
                "start_time": (start_sample / sr),
                "end_time": (end_sample / sr)
            })
            
        print(f"Successfully chunked {audio_id} into {num_chunks} segments.")
        return chunk_info
        
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return []

if __name__ == "__main__":
    # Test on a single file if it exists
    SAMPLE_RAW = "data/raw/audio_samples/raw_0.mp3"
    PROCESSED_BASE = "data/processed/chunks"
    
    if os.path.exists(SAMPLE_RAW):
        preprocess_audio(SAMPLE_RAW, PROCESSED_BASE, 0)
    else:
        print(f"Sample file not found: {SAMPLE_RAW}")
