import os
import requests
import mimetypes
from flask import Blueprint, request, jsonify, send_from_directory
from bs4 import BeautifulSoup

image_bp = Blueprint("image", __name__)
IMAGE_DIR = "static/images"
os.makedirs(IMAGE_DIR, exist_ok=True)


@image_bp.route("/image/<filename>", methods=["GET"])
def serve_images(filename):
    try:
        return send_from_directory(IMAGE_DIR, filename)
    except FileNotFoundError:
        return jsonify({"error": "Image not found"}), 404
