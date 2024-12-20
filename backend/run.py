from flask import Flask

from dotenv import load_dotenv
from flask_cors import CORS
from routes import register_routes


load_dotenv()

app = Flask(__name__)
CORS(app)

register_routes(app)

if __name__ == "__main__":
    app.run(port=5000)
