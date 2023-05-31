from flask import Blueprint, jsonify, request
from firebase_admin import firestore, auth
import requests
import dotenv
import os

authAPI = Blueprint('authAPI', __name__)
db = firestore.client()

@authAPI.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    try:
        users = auth.get_user_by_email(email)
        if users:          
            dotenv.load_dotenv()
            api_key_token= os.getenv("API_KEY_TOKEN")
            firebase_url="https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}".format(api_key_token)
            req = requests.post(firebase_url,json=
                                 {
                                  "email":email , 
                                  "password":password
                                  })
            return jsonify({'message': 'Login Successfully', "data":req.json()})
        else:
            return jsonify({'message': 'Login Failed', 'error': 'User not Found'}), 401
    except Exception as e:
        return jsonify({'message': 'Login Failed', 'error':str(e)}),401

#register
@authAPI.route('/register', methods=['POST'])
def register():

    #program random id

    data = request.get_json().document('admin-{randomid}')

    data['id_account']='admin-{randomid}'
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    data['role']='admin'          
    try:
        # Membuat user baru dengan Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password
        )
        return jsonify({'message': 'Registrasi berhasil', 'id_UID': user.uid})

    except Exception as e:
        return jsonify({'message': 'Registrasi gagal', 'error': str(e)}), 400
