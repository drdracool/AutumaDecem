import os
import requests
import mimetypes
from flask import Blueprint, request, jsonify, send_from_directory
from bs4 import BeautifulSoup

image_bp = Blueprint("image", __name__)
IMAGE_DIR = "static/images"
os.makedirs(IMAGE_DIR, exist_ok=True)


@image_bp.route("/download-image", methods=["POST"])
def download_image():
    image_url = request.json.get("url")
    if not image_url:
        return jsonify({"error": "Image URL is required"}), 400

    try:
        response = requests.get(image_url)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type")
        extension = mimetypes.guess_extension(content_type)
        if not extension:
            extension = ".jpg"

        filename = image_url.split("/")[-1].split("?")[0]
        if not filename.endswith(extension):
            filename += extension
        filepath = os.path.join(IMAGE_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)

        return jsonify({"local_url": f"/static/images/{filename}"})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@image_bp.route("/static/images/<path:filename>")
def serve_images(filename):
    return send_from_directory(IMAGE_DIR, filename)
