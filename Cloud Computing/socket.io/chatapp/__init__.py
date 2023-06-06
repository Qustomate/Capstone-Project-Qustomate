from flask import Flask 

from .events import socketio
from .routes import main 

import firebase_admin
from firebase_admin import credentials, initialize_app, firestore

cred = credentials.Certificate("chatapp/serviceAccountKey.json")

default_app = firebase_admin.initialize_app(cred)

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "secret"

    from .events import events

    app.register_blueprint(events, url_prefix='/events')
    app.register_blueprint(main)

    socketio.init_app(app)

    return app
