from flask import Blueprint, jsonify, request
from firebase_admin import firestore

db = firestore.client()
messageAPI = Blueprint('messageAPI', __name__)

#Tambah Data dengan tambahan field
@messageAPI.route('/add', methods=['POST'])
def add_message():

#get pesan wa

    data = request.get_json()
    message_ref = db.collection('message')

    id_message = data.get('id_message')
    message_text = data.get('message_text')
    senderID = data.get('senderID')
    timestamp = data.get('time_stamp')
    
    #Peanambahan field yang diperlukan
    data['read_status']=False
    data['sentiment_status']=False
    data['positive']=0
    data['negative']=0
    
    #Bagian kesiapa 
    data['chat_id'] = 1
    data['sales'] = 0

 
    message_ref.document().set(data)

    return jsonify({'message': 'Message added successfully'}), 200

#Tampilkan chat terbaru tiap chat client 
#PROMBLEM 1
# @messageAPI.route('/new/<chat_id>', methods=['GET'])
# def get_new_messages_by_chat_id(chat_id):
#     messages_ref = db.collection('message')
#     query = messages_ref.where('chat_id', '==', chat_id).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
#     messages = query.get()

#     all_messages = []
#     for message in messages:
#         message_data = message.to_dict()
#         all_messages.append(message_data)

#     return jsonify(all_messages), 200



#Tampilkan message secara Kondisi setiap chat
@messageAPI.route('/all/<int:chat_id>', methods=['GET'])
def get_messages_by_chat_id(chat_id):
    messages_ref = db.collection('message')
    query = messages_ref.where('chat_id', '==', chat_id).get()

    all_messages = []
    for message in query:
        message_data = message.to_dict()
        all_messages.append(message_data)

    return jsonify(all_messages), 200

#Tampilkan seluruh message pada data base
@messageAPI.route('/all', methods=['GET'])
def get_all_messages():
    messages_ref = db.collection('message')
    messages = messages_ref.get()

    all_messages = []
    for message in messages:
        message_data = message.to_dict()
        all_messages.append(message_data)

    return jsonify(all_messages), 200