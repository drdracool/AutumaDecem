from flask import Blueprint, jsonify, request
from bson import ObjectId
from extensions import db
import requests
import os
from bs4 import BeautifulSoup
import re
import hashlib

post_bp = Blueprint("post", __name__)
posts_collection = db["posts"]
comments_collection = db["comments"]

IMAGE_DIR = "static/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Initialize a set to store existing image file names
existing_images = set()


def initialize_image_cache():
    """Populate the existing_images set with filenames from IMAGE_DIR."""
    global existing_images
    if os.path.exists(IMAGE_DIR):
        existing_images = {
            filename
            for filename in os.listdir(IMAGE_DIR)
            if os.path.isfile(os.path.join(IMAGE_DIR, filename))
        }
        print(f"Existing images loaded: {existing_images}")


@post_bp.route("/titles", methods=["GET"])
def get_titles():
    titles = list(posts_collection.find({}, {"_id": 0, "title": 1, "slug": 1}))
    return jsonify(titles)


@post_bp.route("/post/<slug>", methods=["GET"])
def get_post(slug):
    post = posts_collection.find_one(
        {"slug": slug}, {"_id": 1, "title": 1, "content": 1}
    )

    if not post:
        return jsonify({"error": "Post not found"}), 404

    postId = post["_id"]
    del post["_id"]

    content_html = post.get("content", "")
    # Use BeautifulSoup to parse html content
    soup = BeautifulSoup(content_html, "html.parser")
    images = soup.find_all("img")

    for img in images:
        print(f"Image tag: {img}")
        data_src = img.get("data-src")
        if data_src:
            filename = process_image(data_src, IMAGE_DIR)
            if filename:
                # path separator compatibility & root-relative path
                img["src"] = f"/image/{filename}"
                img["loading"] = "lazy"
            else:
                img["src"] = ""

    post["content"] = str(soup)

    comments = list(
        comments_collection.find({"postId": ObjectId(postId)}, {"_id": 0, "content": 1})
    )

    return jsonify({"post": post, "comments": comments})


def process_image(url, save_dir):
    global existing_images
    cleaned_url = re.sub(r"^[\"\\]+|[\"\\]+$", "", url)

    # Generate a unique filename using a hash
    hash_object = hashlib.md5(cleaned_url.encode("utf-8"))
    hash_hex = hash_object.hexdigest()
    filename = f"{hash_hex}.jpg"

    if filename in existing_images:
        print(f"Image already exists: {filename}")
        return filename

    # Download if the image does not exist
    try:
        response = requests.get(cleaned_url, timeout=5)
        response.raise_for_status()

        filepath = os.path.join(save_dir, filename)

        with open(filepath, "wb") as file:
            file.write(response.content)

        existing_images.add(filename)
        print(f"Image downloaded and saved: {filename}")
        return filename

    except requests.RequestException as e:
        print(f"Failed to download image from {url}: {e}")
        return None


@post_bp.route("/post/<slug>/comment", methods=["POST"])
def add_comment(slug):
    data = request.get_json()
    username = data.get("username")
    content = data.get("content")

    if not username or not content:
        return jsonify({"error": "Username and content are required"}), 400

    post = posts_collection.find_one({"slug": slug}, {"_id": 1})
    if not post:
        return jsonify({"error": "Post not found"}), 404

    new_comment = {
        "postId": ObjectId(post["_id"]),
        "username": username,
        "content": content,
    }

    comments_collection.insert_one(new_comment)
    return jsonify({"message": "Comment added successfully"}), 201


initialize_image_cache()
