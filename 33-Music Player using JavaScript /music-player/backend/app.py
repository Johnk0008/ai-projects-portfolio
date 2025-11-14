from flask import Flask, send_file, jsonify
from flask_cors import CORS
import os
import glob

app = Flask(__name__)
CORS(app)

# Configuration
MUSIC_FOLDER = 'music'
app.config['MUSIC_FOLDER'] = MUSIC_FOLDER

# Sample music data
MUSIC_LIBRARY = [
    {
        "id": 1,
        "title": "Sample Song 1",
        "artist": "Artist 1",
        "file": "sample1.mp3",
        "duration": "0:03"
    },
    {
        "id": 2,
        "title": "Sample Song 2",
        "artist": "Artist 2",
        "file": "sample2.mp3",
        "duration": "0:09"
    },
    {
        "id": 3,
        "title": "Sample Song 3",
        "artist": "Artist 3",
        "file": "sample3.mp3",
        "duration": "0:09"
    }
]

@app.route('/')
def home():
    return jsonify({"message": "Music Player API is running!"})

@app.route('/api/songs')
def get_songs():
    return jsonify(MUSIC_LIBRARY)

@app.route('/api/song/<int:song_id>')
def get_song(song_id):
    song = next((s for s in MUSIC_LIBRARY if s['id'] == song_id), None)
    if song:
        return jsonify(song)
    return jsonify({"error": "Song not found"}), 404

@app.route('/music/<filename>')
def serve_music(filename):
    try:
        return send_file(os.path.join(app.config['MUSIC_FOLDER'], filename))
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    # Create music folder if it doesn't exist
    if not os.path.exists(MUSIC_FOLDER):
        os.makedirs(MUSIC_FOLDER)
        print(f"Created {MUSIC_FOLDER} folder. Please add your MP3 files there.")
    
    app.run(debug=True, port=5000)