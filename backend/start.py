from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
users_collection = db["users"]


@app.route("/api/users", methods=["GET"])
def get_users():
    users = users_collection.find()
    user_list = []
    for user in users:
        user_list.append({"id": user["id"], "name": user["name"]})
    return jsonify(user_list)


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = {"id": data["id"], "name": data["name"]}
    users_collection.insert_one(new_user)
    return jsonify(new_user), 201


if __name__ == "__main__":
    app.run()
