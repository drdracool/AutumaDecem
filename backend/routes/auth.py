from flask import Blueprint, request, jsonify, redirect, url_for, flash
from models.user import User
from werkzeug.security import generate_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")
        print(f"Login attempt with email: {email}")

        user = User.find_by_email(email)
        if not user:
            print("User not found.")
            return jsonify({"error": "Invalid username or password"}), 401

        print(f"User found: {user.email}")

        if not user.check_password(password):
            print("Password check failed.")
            return jsonify({"error": "Invalid username or password"}), 401

        print("Login successful.")
        return jsonify({"message": "Login successful"}), 200
    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({"error": "An error occurred during login"}), 500


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if User.find_by_email(email):
        return jsonify({"error": "User already exists"}), 400

    new_user = User(
        username=username, email=email, password_hash=generate_password_hash(password)
    )
    new_user.save_to_db()
    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/logout")
def logout():
    return "Logout"
