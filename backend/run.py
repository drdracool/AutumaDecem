from flask import Flask
import os
from dotenv import load_dotenv
from flask_cors import CORS
from routes import register_routes
from extensions import db
from flask_jwt_extended import JWTManager
from flask_mail import Mail


load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret-key"
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))  # 默认 587
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True") == "True"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["FRONTEND_URL"] = os.getenv("FRONTEND_URL")
jwt = JWTManager(app)
mail = Mail(app)

CORS(app)

register_routes(app)

if __name__ == "__main__":
    app.run(port=5000)
