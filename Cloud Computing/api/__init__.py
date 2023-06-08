from flask import Flask
from firebase_admin import credentials,initialize_app
import requests
from dotenv import load_dotenv
import os

cred = credentials.Certificate("api/serviceAccountKey2.json")

default_app= initialize_app(cred)

def create_app():

    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY_CONFIG")
    
    from .messageAPI import messageAPI
    # from .sentimentResultAPI import sentimentResultAPI
    from .authAPI import authAPI
    from .DashboardAPI import DashboardAPI
    from .managementAPI import managementAPI
    @app.route('/',methods=['GET'])
    def default():
        return 'Response Success'
    app.register_blueprint(managementAPI, url_prefix='/management')
    app.register_blueprint(DashboardAPI, url_prefix='/dashboard')
    app.register_blueprint(authAPI, url_prefix='/auth')
    app.register_blueprint(messageAPI, url_prefix='/message')
    # app.register_blueprint(sentimentResultAPI, url_prefix='/sentiment-result')
    return app
