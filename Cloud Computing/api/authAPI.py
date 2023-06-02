from flask import Blueprint, jsonify, request
from firebase_admin import firestore, auth
import requests
import dotenv
import os
import uuid

authAPI = Blueprint('authAPI', __name__)
db = firestore.client()
sales_ref = db.collection('sales') 
admin_ref = db.collection('admin') 

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
            #get pencarian firstname atau id dari email diatas
            #id_user
            return jsonify({'message': 'Login Successfully', "data":req.json()})
        else:
            return jsonify({'message': 'Login Failed', 'error': 'User not Found'}), 401
    except Exception as e:
        return jsonify({'message': 'Login Failed', 'error':str(e)}),401

#register
@authAPI.route('/register', methods=['POST'])
def register():

    #program random id
    
    data = request.get_json()   
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    company = data.get('company')
    role = data.get('role')         
    try:
        # Membuat user baru dengan Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password
        )
        random_number = str(uuid.uuid4())[:15]
        #if jika memilih role sales maka masukan sebuah sales_id dengan format nilai "sales-{randomid sebanyak }"
        if role == "sales":
            sales_id = "sales-"+random_number
            if not sales_ref.document(sales_id).get().exists:
                sales_data = {
                    'email':email,
                    'password':password,
                    'client_handler':0,
                    'firstname':first_name ,
                    'lastname': last_name,
                    'role':'sales',
                    'sales_id': sales_id,
                    'company':company,
                    'created':firestore.SERVER_TIMESTAMP
                    
                }
                sales_ref.document(sales_id).set(sales_data)
                return jsonify({'message': 'Registrasi Sales berhasil', 'id_UID': user.uid})
        else :
            admin_id = "admin-"+random_number
            if not sales_ref.document(admin_id).get().exists:
                admin_data = {
                    'email':email,
                    'password':password,
                    'firstname':first_name ,
                    'lastname': last_name,
                    'role':'admin',
                    'admin_id': admin_id,
                    'company':company,
                    'created':firestore.SERVER_TIMESTAMP
                }
                admin_ref.document(admin_id).set(admin_data)
                return jsonify({'message': 'Registrasi Admin berhasil', 'id_UID': user.uid})
            return jsonify({'message': 'salah role'}), 400
    except Exception as e:
        return jsonify({'message': 'Registrasi gagal', 'error': str(e)}), 400
