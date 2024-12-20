from flask import Flask, jsonify, request, render_template, url_for, redirect
from .post import post_bp
from .image import image_bp


def register_routes(app: Flask):
    app.register_blueprint(post_bp, url_prefix="/")
    app.register_blueprint(image_bp, url_prefix="/")
