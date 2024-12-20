from flask import Blueprint, jsonify, request
from bson import ObjectId
from extensions import db
import requests
import os
from bs4 import BeautifulSoup

post_bp = Blueprint("post", __name__)
posts_collection = db["posts"]
comments_collection = db["comments"]

IMAGE_DIR = "static/images"
os.makedirs(IMAGE_DIR, exist_ok=True)


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
    # use BeautifulSoup to parse html content
    soup = BeautifulSoup(content_html, "html.parser")
    images = soup.find_all("img")

    for img in images:
        data_src = img.get("data-src")
        if data_src:
            try:
                response = requests.get(data_src)
                response.raise_for_status()

                content_type = response.headers.get("Content-Type")
                extension = mimetypes.guess_extension(content_type)
                if not extension:
                    extension = ".jpg"

                filename = os.path.basename(data_src.split("?")[0])
                if not filename.endswith(extension):
                    filename += extension
                filepath = os.path.join(IMAGE_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(response.content)

                img["src"] = f"/static/images/{filename}"
            except requests.RequestException as e:
                print(f"Failed to download image: {data_src}, error: {e}")
                img["src"] = ""

    post["content"] = str(soup)

    comments = list(
        comments_collection.find({"postId": ObjectId(postId)}, {"_id": 0, "content": 1})
    )

    return jsonify({"post": post, "comments": comments})


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
