from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

users_collection = db["users"]


class User:
    def __init__(self, username, email, password=None, password_hash=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash or (
            generate_password_hash(password) if password else None
        )

    def save_to_db(self):
        try:
            result = users_collection.insert_one(
                {
                    "username": self.username,
                    "email": self.email,
                    "password_hash": self.password_hash,
                }
            )
            print(f"User saved successfully with ID: {result.inserted_id}")
        except Exception as e:
            print(f"Error saving user to database: {str(e)}")

    @staticmethod
    def find_by_email(email):
        data = users_collection.find_one({"email": email})
        if data:
            return User(
                username=data["username"],
                email=data["email"],
                password_hash=data["password_hash"],
            )
        return None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
