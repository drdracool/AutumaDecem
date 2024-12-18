from flask import Flask, jsonify, request, render_template, url_for, redirect
from pymongo import MongoClient
import json
from dotenv import load_dotenv
from flask_cors import CORS
from bson import ObjectId


load_dotenv()
app = Flask(__name__)
CORS(app)
# app.config.from_prefixed_env("MYAPP")
client = MongoClient("localhost", 27017)
db = client.flask_db
arcitles = db.articles


client = MongoClient("mongodb://localhost:27017/")
db = client["blog"]
posts_collection = db["posts"]
comments_collection = db["comments"]


@app.route("/titles", methods=["GET"])
def get_titles():
    titles = list(posts_collection.find({}, {"_id": 0, "title": 1, "slug": 1}))
    return jsonify(titles)


@app.route("/post/<slug>", methods=["GET"])
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


@app.route("/post/<slug>/comment", methods=["POST"])
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


if __name__ == "__main__":
    app.run(port=5000)
