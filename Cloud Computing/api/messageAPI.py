from flask import Blueprint, jsonify, request
from firebase_admin import firestore
import uuid

db = firestore.client()

messageAPI = Blueprint('messageAPI', __name__)

message_ref = db.collection('message')
chat_ref = db.collection('chat')
sales_ref = db.collection('Sales')

#Tambah Data dengan tambahan field
@messageAPI.route('/add', methods=['POST'])
def add_message():
    try:
    #get pesan wa
        data = request.get_json()
        id_message = data.get('id_message')
        message_text = data.get('message_text')
        sender_id = data.get('sender_id')
        timestamp = data.get('time_stamp')

        #Peanambahan field yang diperlukan
        data['read_status']=False
        #FUNGSI SENTIMENT ML NYA 


        # funngsi sentiment_analyis(data.get(message_text))
        data['positive']=0
        data['negative']=0
        query = message_ref.where('sender_id', '==',sender_id).get()
        if not query:
            #ROTATOR SALES
            sales_query = sales_ref.order_by('client_handler').limit(1).get()
            if sales_query:
                sales_id = sales_query[0].id
                client_handler = sales_query[0].get('client_handler')
                # Increment client_handler by 1
                client_handler += 1
                # Update the document with the new client_handler value
                sales_ref.document(sales_id).update({'client_handler': client_handler})
                # Retrieve the data from the request
                # Add sales_id to the data
                data['sales_id'] = sales_id   
            else :
                data['sales_id'] = 'sales-12345678'
            #Buat chat baru  
            random_number = str(uuid.uuid4())[:15]
            chat_id = "chat-"+random_number
            if not chat_ref.document(chat_id).get().exists:            
                chat_data = {
                    'alamat':'-',
                    'catatan':'-',
                    'chat_id': chat_id,
                    'kota':'-',
                    'name':'-',
                    'produk':'-',
                    'revenue':0,
                    'sender_id':sender_id,
                    'sales_id': sales_id,
                    'status': 'baru'
                }
                data['chat_id']=chat_id
                chat_ref.document(chat_id).set(chat_data)
            message_ref.document().set(data)
            data['sender_id']= sender_id
            return jsonify({'message': 'Message & Chat added successfully'},data), 200
        data['sender_id']= sender_id
        message_ref.document().set(data)
        return jsonify({'message': 'Message added successfully'},data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

#Tampilkan message secara Kondisi setiap chat
@messageAPI.route('/all/<string:chat_id>', methods=['GET'])
def get_messages_by_chat_ids(chat_id):
    try:
        message_ref = db.collection('message')
        query = message_ref.where('chat_id', '==', chat_id).get()
        all_messages = []
        for message in query:
            message_data = message.to_dict()
            all_messages.append(message_data)
        return jsonify(all_messages), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
#Tampilkan seluruh message pada data base
@messageAPI.route('/all', methods=['GET'])
def get_all_messages():
    messages = message_ref.get()
    all_messages = []
    for message in messages:
        message_data = message.to_dict()
        all_messages.append(message_data)

    return jsonify(all_messages), 200
