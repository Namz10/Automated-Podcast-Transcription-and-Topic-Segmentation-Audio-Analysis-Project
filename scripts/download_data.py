import pandas as pd
import requests
import os
import librosa
import soundfile as sf
from tqdm import tqdm
import time

def download_podcasts(csv_path, output_dir, limit=200):
    print(f"Reading dataset from {csv_path}...")
    df = pd.read_csv(csv_path, nrows=limit)
    
    os.makedirs(output_dir, exist_ok=True)
    
    downloaded_files = []
    
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Downloading Podcasts"):
        audio_url = row['pod_link']
        audio_id = row[0]  # First column is the ID
        
        # Determine file path
        # Some URLs might not have a clear extension, we'll default to .mp3 and handle it in processing
        file_path = os.path.join(output_dir, f"raw_{audio_id}.mp3")
        
        if os.path.exists(file_path):
            downloaded_files.append(file_path)
            continue

        try:
            # Downloading first 2MB as a sample to keep it manageable for Milestone 1
            with requests.get(audio_url, stream=True, timeout=10) as r:
                r.raise_for_status()
                with open(file_path, 'wb') as f:
                    size = 0
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            size += len(chunk)
                        if size > 2 * 1024 * 1024:  # 2MB Limit
                            break
            downloaded_files.append(file_path)
        except Exception as e:
            print(f"Failed to download {audio_url}: {e}")
            
    print(f"Successfully downloaded {len(downloaded_files)} samples to {output_dir}")
    return downloaded_files

if __name__ == "__main__":
    CSV_PATH = "data/raw/audio/politicalpodcasts.csv"
    OUTPUT_DIR = "data/raw/audio_samples"
    download_podcasts(CSV_PATH, OUTPUT_DIR, limit=200)
