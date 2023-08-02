from flask import Flask, request
from .api import chat


app=Flask(__name__)


app.register_blueprint(chat)


def get_app():
    return app