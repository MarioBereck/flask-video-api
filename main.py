import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # permite acesso do React Native

# Caminho da pasta onde estão os vídeos
VIDEO_FOLDER = os.path.join(os.path.dirname(__file__), "video")

@app.route("/")
def home():
    return "<h1>🎥 API de Vídeos Flask</h1><p>Use /media/video para listar os vídeos.</p>"

@app.route("/media/video", methods=["GET"])
def list_videos():
    """
    Lista todos os vídeos disponíveis na pasta /video
    """
    videos = []

    if not os.path.exists(VIDEO_FOLDER):
        os.makedirs(VIDEO_FOLDER)

    for filename in os.listdir(VIDEO_FOLDER):
        if filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
            videos.append({
                "name": filename,
                "url": f"http://10.72.109.23:8080/media/video/{filename}"
            })

    return jsonify({"videos": videos})


@app.route("/media/video/<path:filename>")
def serve_video(filename):
    """
    Serve um arquivo de vídeo específico.
    Exemplo: http://10.72.109.23:8080/media/video/meuvideo.mp4
    """
    return send_from_directory(VIDEO_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
