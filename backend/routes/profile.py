from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_username = get_jwt_identity()
    if current_username:
        return (
            jsonify(
                {
                    "username": current_username,
                }
            ),
            200,
        )
    else:
        return jsonify({"message": "User not found"}), 404
