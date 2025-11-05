import os
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # permite acesso do React Native

# inicializa o Swagger
swagger = Swagger(app)

# Caminho da pasta onde estão os vídeos
VIDEO_FOLDER = os.path.join(os.path.dirname(__file__), "video")

@app.route("/")
def home():
    """
    Página inicial da API
    ---
    responses:
      200:
        description: Página inicial da API de vídeos
        content:
          text/html:
            example: <h1>🎥 API de Vídeos Flask</h1><p>Use /media/video para listar os vídeos.</p>
    """
    return "<h1>🎥 API de Vídeos Flask</h1><p>Use /media/video para listar os vídeos.</p>"

@app.route("/media/video", methods=["GET"])
def list_videos():
    """
    Lista todos os vídeos disponíveis na pasta /video
    ---
    responses:
      200:
        description: Lista de vídeos encontrados
        schema:
          type: object
          properties:
            videos:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                    example: meuvideo.mp4
                  url:
                    type: string
                    example: http://127.0.0.1:8080/media/video/meuvideo.mp4
    """
    videos = []

    if not os.path.exists(VIDEO_FOLDER):
        os.makedirs(VIDEO_FOLDER)

    for filename in os.listdir(VIDEO_FOLDER):
        if filename.lower().endswith((".mp4", "mp3", ".mov", ".avi", ".mkv")):
            videos.append({
                "name": filename,
                # usa a URL dinâmica baseada no domínio atual
                "url": f"{request.url_root}media/video/{filename}"
            })

    return jsonify({"videos": videos})

@app.route("/media/video/<path:filename>")
def serve_video(filename):
    """
    Serve um arquivo de vídeo específico.
    ---
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        description: Nome do arquivo de vídeo
    responses:
      200:
        description: Retorna o arquivo de vídeo solicitado
      404:
        description: Arquivo não encontrado
    """
    return send_from_directory(VIDEO_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
