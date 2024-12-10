from flask import Flask, jsonify, request, render_template, url_for, redirect
from pymongo import MongoClient
import json
from dotenv import load_dotenv
from flask_cors import CORS

CORS(app)

load_dotenv()
app = Flask(__name__)
# app.config.from_prefixed_env("MYAPP")
client = MongoClient("localhost", 27017)
db = client.flask_db
arcitles = db.articles


client = MongoClient("mongodb://localhost:27017/")
db = client["blog"]
users_collection = db["posts"]


@app.route("/titles", methods=["GET"])
def get_titles():
    titles = list(users_collection.find({}, {"_id": 0, "title": 1}))
    return jsonify(titles)


@app.route("/<url>", methods=["GET"])
def get_post(url):
    post = users_collection.find_one({"url": url}, {"_id": 0, "title": 1, "content": 1})

    if not post:
        return jsonify({"error": "Post not found"}), 404

    return jsonify(post)


if __name__ == "__main__":
    app.run(port=5000)
