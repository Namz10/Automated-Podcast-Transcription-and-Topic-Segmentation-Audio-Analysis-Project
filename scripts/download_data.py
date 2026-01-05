import requests
import os
import xml.etree.ElementTree as ET
import librosa
import soundfile as sf
import tempfile

def download_from_rss():
    rss_url = "https://lexfridman.com/feed/podcast/"
    print(f"Fetching RSS feed from {rss_url}...")
    
    try:
        response = requests.get(rss_url)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        item = root.find(".//item")
        enclosure = item.find("enclosure")
        audio_url = enclosure.get("url")
        
        print(f"Found audio URL: {audio_url}")
        
        raw_audio_dir = "data/raw/audio"
        os.makedirs(raw_audio_dir, exist_ok=True)
        
        final_wav = os.path.join(raw_audio_dir, "episode_sample.wav")
        
        # We'll download the first 5MB to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name
            print(f"Downloading first 5MB of audio to {tmp_path}...")
            with requests.get(audio_url, stream=True) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=8192):
                    tmp.write(chunk)
                    if os.path.getsize(tmp_path) > 5 * 1024 * 1024:
                        break
        
        print(f"Loading and trimming with librosa...")
        # Load first 60 seconds
        # Librosa might still struggle with mp3 if soundfile doesn't support it
        # But we'll try it. 
        y, sr = librosa.load(tmp_path, duration=60, sr=16000)
        
        print(f"Saving to {final_wav}...")
        sf.write(final_wav, y, sr)
        
        os.remove(tmp_path)
        print(f"Successfully saved 60s sample to {final_wav}")
        
    except Exception as e:
        print(f"Error: {e}")
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    download_from_rss()
