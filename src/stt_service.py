import whisper
import json
import os
import librosa

def transcribe_audio(file_path, model_name="base", output_dir="data/transcripts"):
    print(f"Loading Whisper model: {model_name}...")
    model = whisper.load_model(model_name)
    
    print(f"Loading audio with librosa: {file_path}...")
    # Whisper expects 16kHz mono audio
    audio_array, _ = librosa.load(file_path, sr=16000, mono=True)
    
    print(f"Transcribing array...")
    # transcribe can accept a numpy array
    result = model.transcribe(audio_array, verbose=False)
    
    # Save the full result as JSON for further processing (timestamps, etc.)
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.basename(file_path).replace(".wav", ".json")
    output_path = os.path.join(output_dir, base_name)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    
    print(f"Transcription complete. Saved to: {output_path}")
    
    # Extract just the text for a quick look
    text_path = output_path.replace(".json", ".txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
        
    return result

if __name__ == "__main__":
    transcribe_audio("data/processed/episode_sample_cleaned.wav", model_name="base")
