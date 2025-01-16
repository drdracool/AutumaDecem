from flask import Flask

from dotenv import load_dotenv
from flask_cors import CORS
from routes import register_routes
from extensions import db
from flask_jwt_extended import JWTManager

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret-key"
jwt = JWTManager(app)
CORS(app)

register_routes(app)

if __name__ == "__main__":
    app.run(port=5000)
