import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SEGMENTED_DIR = "data/segmented"

METADATA_FILE = "data/podcast_metadata.json"

def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def load_podcast_data(podcast_id):
    path = os.path.join(SEGMENTED_DIR, f"{podcast_id}_segmented.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

@app.route("/api/podcasts", methods=["GET"])
def get_podcasts():
    """Returns a list of available podcasts with basic metadata."""
    metadata = load_metadata()
    processed_podcasts = []
    
    # List all files in segmented dir to find what's ready
    processed_files = os.listdir(SEGMENTED_DIR)
    processed_ids = [f.split('_')[0] for f in processed_files if f.endswith('_segmented.json')]
    
    for item in metadata:
        pid = str(item["id"])
        if pid in processed_ids:
            data = load_podcast_data(pid)
            if data:
                processed_podcasts.append({
                    "id": pid,
                    "title": item["title"],
                    "domain": item["domain"],
                    "segment_count": len(data),
                    "preview_summary": data[0]["summary"] if data else ""
                })
    return jsonify(processed_podcasts)

@app.route("/api/podcast/<podcast_id>", methods=["GET"])
def get_podcast_details(podcast_id):
    """Returns the full segmented data for a specific podcast."""
    data = load_podcast_data(podcast_id)
    if data:
        return jsonify(data)
    return jsonify({"error": "Podcast not found"}), 404

@app.route("/api/search", methods=["GET"])
def search():
    """Searches for segments containing the query string across all podcasts."""
    query = request.args.get("q", "").lower()
    if not query:
        return jsonify([])
    
    results = []
    metadata = load_metadata()
    processed_files = os.listdir(SEGMENTED_DIR)
    processed_ids = [f.split('_')[0] for f in processed_files if f.endswith('_segmented.json')]
    
    metadata_map = {str(m["id"]): m for m in metadata}

    for pid in processed_ids:
        data = load_podcast_data(pid)
        if data:
            m_info = metadata_map.get(pid, {"title": f"Podcast {pid}"})
            for seg in data:
                # Search in text, keywords, and summary
                if (query in seg["text"].lower() or 
                    any(query in kw.lower() for kw in seg["keywords"]) or 
                    query in seg["summary"].lower()):
                    
                    results.append({
                        "podcast_id": pid,
                        "podcast_title": m_info["title"],
                        "segment_id": seg["segment_id"],
                        "summary": seg["summary"],
                        "keywords": seg["keywords"],
                        "text": seg["text"]
                    })
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
