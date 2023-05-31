from flask import Flask
from firebase_admin import credentials,initialize_app

cred = credentials.Certificate("api/serviceAccountKey.json")

default_app=initialize_app(cred)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'isatarmana001'
    
    from .messageAPI import messageAPI
    from .sentimentResultAPI import sentimentResultAPI
    from .authAPI import authAPI

    app.register_blueprint(authAPI, url_prefix='/auth')
    app.register_blueprint(messageAPI, url_prefix='/message')
    app.register_blueprint(sentimentResultAPI, url_prefix='/sentiment-result')
    return app



   
   
# @app.route('/')
# def index():
# return '<h1>hello 1</h1>'



#inisiasi flask nya

