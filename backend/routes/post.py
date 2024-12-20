from flask import Blueprint, jsonify, request
from bson import ObjectId
from extensions import db

post_bp = Blueprint("post", __name__)
posts_collection = db["posts"]
comments_collection = db["comments"]


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
