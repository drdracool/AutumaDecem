from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

users_collection = db["users"]


class User:
    def __init__(
        self,
        username,
        email,
        password_hash=None,
        is_active=False,
        activation_token=None,
        activated_at=None,
        created_at=None,
    ):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_active = is_active
        self.activation_token = activation_token
        self.activated_at = activated_at
        self.created_at = created_at if created_at else datetime()

    def save_to_db(self):
        try:
            result = users_collection.insert_one(
                {
                    "username": self.username,
                    "email": self.email,
                    "password_hash": self.password_hash,
                    "is_active": self.is_active,
                    "activation_token": self.activation_token,
                    "activated_at": self.activated_at,
                    "created_at": self.created_at,
                }
            )
            print(f"User saved successfully with ID: {result.inserted_id}")
        except Exception as e:
            print(f"Error saving user to database: {str(e)}")

    @staticmethod
    def find_by_email(email):
        data = users_collection.find_one({"email": email}, {"_id": 0, "email": 1})
        return data

    @staticmethod
    def find_by_activation_token(activation_token):
        hashed_token = generate_password_hash(activation_token)
        data = users_collection.find_one({"activation_token": hashed_token})
        if data:
            if check_password_hash(data["activation_token"], activation_token):
                return User(
                    is_active=data["is_active"],
                    activation_token=data["activation_token"],
                    activated_at=data["activated_at"],
                )
        return None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
