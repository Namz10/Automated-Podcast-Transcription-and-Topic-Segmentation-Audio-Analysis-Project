import whisper
import json
import os
import glob
import re
from tqdm import tqdm
from static_ffmpeg import add_paths

# Add ffmpeg to the path
add_paths()

def clean_text(text):
    """
    Performs basic text cleaning:
    - Removes filler words (um, uh, etc.) - simple regex
    - Basic punctuation and spacing normalization
    """
    # Simple list of filler words
    fillers = r'\b(um|uh|err|ah|like|you know|sort of|kind of)\b'
    text = re.sub(fillers, '', text, flags=re.IGNORECASE)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def transcribe_chunks(chunks_dir, audio_id, model_name="base", output_dir="data/transcripts"):
    """
    Transcribes all chunks for a given audio_id and aggregates results.
    """
    print(f"Loading Whisper model: {model_name}...")
    model = whisper.load_model(model_name)
    
    chunk_files = sorted(glob.glob(os.path.join(chunks_dir, str(audio_id), "*.wav")))
    
    if not chunk_files:
        print(f"No chunks found for audio_id: {audio_id}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    full_transcript = []
    
    for chunk_file in tqdm(chunk_files, desc=f"Transcribing chunks of {audio_id}"):
        # We can extract chunk index from filename if needed
        # result = model.transcribe(chunk_file, verbose=False)
        result = model.transcribe(chunk_file, verbose=False) # Whisper usually handles array or path
        
        # Each 'segment' in result['segments'] has start/end relative to the chunk
        # We need to offset them by the chunk's global start time if we want a global transcript
        # For Milestone 1, we just need to preserve them as is per chunk, or aggregate them.
        
        cleaned_text = clean_text(result["text"])
        
        chunk_data = {
            "chunk_file": os.path.basename(chunk_file),
            "text": cleaned_text,
            "segments": result["segments"]
        }
        full_transcript.append(chunk_data)
        
    output_path = os.path.join(output_dir, f"{audio_id}_transcript.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(full_transcript, f, indent=4, ensure_ascii=False)
        
    print(f"Transcription for {audio_id} complete. Saved to: {output_path}")
    return full_transcript

if __name__ == "__main__":
    # Test on the first processed audio_id
    CHUNKS_DIR = "data/processed/chunks"
    AUDIO_ID = 0
    if os.path.exists(os.path.join(CHUNKS_DIR, str(AUDIO_ID))):
        transcribe_chunks(CHUNKS_DIR, AUDIO_ID, model_name="base")
    else:
        print(f"No chunks to transcribe for ID {AUDIO_ID}")
