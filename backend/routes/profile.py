from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    jwt_claims = get_jwt()
    username = jwt_claims.get("username")
    if username:
        return (
            jsonify(
                {
                    "username": username,
                }
            ),
            200,
        )
    else:
        return jsonify({"message": "User not found"}), 404
