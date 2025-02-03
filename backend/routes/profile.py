from flask import Blueprint, jsonify, request
from bson import ObjectId
from extensions import db
import requests
import os
from bs4 import BeautifulSoup
import re
import hashlib
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user_email = get_jwt_identity()
    user = User.find_by_email(current_user_email)

    if user:
        return (
            jsonify(
                {
                    "name": user.username,
                }
            ),
            200,
        )
    else:
        return jsonify({"message": "User not found"}), 404
