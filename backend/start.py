from flask import Flask, jsonify, request, render_template, url_for, redirect
from pymongo import MongoClient
import json
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
# app.config.from_prefixed_env("MYAPP")
client = MongoClient("localhost", 27017)
db = client.flask_db
arcitles = db.articles


client = MongoClient("mongodb://localhost:27017/")
db = client["blog"]
users_collection = db["posts"]


@app.route("/", methods=("GET", "POST"))
def index():
    posts = list(users_collection.find({}, {"_id": 0, "title": 1, "content": 1}))
    return jsonify(posts)


if __name__ == "__main__":
    app.run(port=5000)
