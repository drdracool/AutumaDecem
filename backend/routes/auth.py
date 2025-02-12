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
import os
import secrets
from flask_mail import Mail, Message
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

auth_bp = Blueprint("auth", __name__)
mail = Mail()


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

    activation_token = secrets.token_urlsafe(32)

    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        is_active=False,
        activation_token=activation_token,
    )
    new_user.save_to_db()

    activation_link = (
        f"{current_app.config['FRONTEND_URL']}/activate/{activation_token}"
    )
    send_activation_email(email, activation_link)

    return (
        jsonify(
            {
                "message": "Account created. Please check your email to activate your account."
            }
        ),
        201,
    )


def send_activation_email(to_email, activation_link):
    brevo_api_key = os.getenv("BREVO_API_KEY")
    if not brevo_api_key:
        raise ValueError("BREVO_API_KEY not set")

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = brevo_api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    sender = {"name": "Autuma-Decem", "email": os.getenv("MAIL_DEFAULT_SENDER")}
    subject = "Activate Your Account"
    html_content = f"""
    <html>
    <body>
        <p>Hi,</p>
        <p>Thank you for registering. Please click the link below to activate your account:</p>
        <a href="{activation_link}">Activate Account</a>
    </body>
    </html>
    """
    to = [{"email": to_email}]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, sender=sender, subject=subject, html_content=html_content
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Email sent successfully: {api_response}")
    except ApiException as e:
        print(f"Error sending email: {e}")


@auth_bp.route("/activate/<token>", methods=["GET"])
def activate_account(token):
    user = User.find_by_activation_token(token)

    if not user:
        return jsonify({"error": "Invalid or expired token"}), 400

    user.is_active = True
    user.activation_token = None
    user.save_to_db()

    return (
        jsonify({"message": "Account activated successfully. You can now log in."}),
        200,
    )


@auth_bp.route("/logout")
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response
