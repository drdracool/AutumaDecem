from flask import Blueprint, request, jsonify, redirect, url_for, flash
from models.user import User
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required,
    JWTManager,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")
        remember = data.get("remember", False)
        print(f"Login attempt with email: {email}")

        user = User.find_by_email(email)
        if not user:
            print("User not found.")
            return jsonify({"error": "User not found"}), 401

        print(f"User found: {user.email}")

        if not user.check_password(password):
            print("Password check failed.")
            return jsonify({"error": "Invalid username or password"}), 401

        print("Login successful.")
        # Generate access token valid for an hour
        expires = timedelta(days=30) if remember else timedelta(hours=1)
        access_token = create_access_token(
            expires_delta=expires,
            identity=user.email,
            additional_claims={"username": user.username},
        )
        return jsonify({"token": access_token}), 200
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
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response
