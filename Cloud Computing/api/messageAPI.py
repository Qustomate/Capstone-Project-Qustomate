from flask import Blueprint, jsonify, request
from firebase_admin import firestore
from datetime import datetime,timedelta
import uuid

#memanggil fungsi dan variabel yang diperlukan pada file function.py agar mempermudah penulisan codenya
from .function import id_checker_sales, sales_ref, chat_ref, message_ref ,id_checker_message,generate_rdm_id, db
#memanggil fungsi prediksi sentiment 
from .sentimentResultAPI import predict_sentiment

messageAPI = Blueprint('messageAPI', __name__) #mendefinisikan blueprint dalam penggunaan enpoint message

#Tambahkan data pesan ke collection message 
@messageAPI.route('/add', methods=['POST'])
def add_message():
    try:
#DEFINISI VARIABEL YANG DIPERLUKAN
        
    #Request Enpoint WA(dikerjakan)

    #---
        """
        Skema mengambil dari postman dengan data sementara(beta)
        """
    #mengambil inputan ke server       
        id_message = request.json['id_message']
        timestamp_str = request.json['time_stamp']        
        message_text  = request.json['message_text']
        sender_id  = request.json['sender_id']
        timestamp_str = request.json['time_stamp']
        recipientID = request.json['recipientID']

    #membuat dokumen message pada collection message dengan id_message untuk menampung data pesan
        id_checker_message(id_message)  #check Id Message
        message_doc = message_ref.document(id_message)  #membuat variabel dokumen
        #mengubah string format waktu agar dapat dibaca oleh firestore
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S") 
#----
#MACHINE LEARNING SENTIMENT ANALYSIS
        sentiment_result = predict_sentiment(message_text)
        if sentiment_result < 0.6:
            sentiment = 'negative'
        else :
            sentiment = 'positive'

#----
#PEMBUATAN CHAT
        """
        Logika pembuatan chat dibuat saat sender_id atau client memulai chat kepada nomor perusahaan,
        selain itu terdapat Rotator penugasan kepada Sales-sales di perusahaan agar pelayanan Client merata
        saat ada client baru dan memberikan tempan untuk pesan-pesan antara client dan sales
        """
        #pencarian inputan sender_id sama dengan yang di database
        sender_query = message_ref.where('sender_id', '==',sender_id).get()
        #kondisi yang dilakukan jika sender_id tidak ada di database atau client baru
        if not sender_query:

    #ROTATOR SALES
            #Query untuk mengambil sales yang melayani client paling sedikit 
            sales_query = sales_ref.order_by('client_handler').limit(1).get()
            
            if sales_query:
                sales_id = sales_query[0].id    #ambil id sales tersebut

                client_handler = sales_query[0].get('client_handler')   #ambil client_handler terakhir dihandler
                client_handler += 1     #increment client yang ditangani
                # mengupdate banyaknya client yang ditangani
                sales_ref.document(sales_id).update({'client_handler': client_handler})
    #----
    #Create Chat
             
            chat_id = generate_rdm_id("chat-") #membuat id chat yang berbeda       

            #membuat field defaut untuk setiap chat baru                        
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
                'status': 'baru',
                'first_timestamp':timestamp,
                'last_timestamp':timestamp,
                'catatan':'-',
                'new_message_count':1
            }
            #mengirimkan data pesan ke database
            message_doc.set({
            "id_message": id_message,
            "time_stamp": timestamp,
            "read_status": False,
            "recopoentID": recipientID,
            "sales_id": sales_id,
            "sender_id": sender_id,
            "sentiment": sentiment,
            "chat_id":chat_id,
            "message_text":message_text
            })

            # mengirimkan chat default dokumen ke database
            chat_ref.document(chat_id).set(chat_data)
            
            
            return jsonify({'message': 'Message & Chat added successfully'},{
            "id_message": id_message,
            "time_stamp": timestamp,
            "read_status": False,
            "recopoentID": recipientID,
            "sales_id": sales_id,
            "sender_id": sender_id,
            "sentiment": sentiment,
            "chat_id":chat_id,
            "message_text":message_text
            }), 200
     
        
        #mengambil nilai di field chat_id pada collection chat bedasarkan field sender_id
        query = chat_ref.where('sender_id', '==', sender_id).get()
        chat_ids = []
        sales_ids=[]
        for doc in query:
            chat_data = doc.to_dict()
            chat_ids.append(chat_data['chat_id'])
            sales_ids.append(chat_data['sales_id'])
        chat_ids_string = ','.join(chat_ids)  # Mengubah list chat_ids menjadi string dengan pemisah koma
        sales_ids_string = ','.join(sales_ids)        
        
        chat_ref.document(chat_ids_string).update({'last_timestamp':timestamp })


        message_doc.set({
            "id_message": id_message,
            "time_stamp": timestamp,
            "read_status": False,
            "recopoentID": recipientID,
            "sales_id": sales_ids_string,
            "sender_id": sender_id,
            "sentiment": sentiment,
            "chat_id":chat_ids_string,
            "message_text":message_text
        })
        return jsonify({'message': 'Message added successfully'},{
            "id_message": id_message,
            "time_stamp": timestamp,
            "read_status": False,
            "recopoentID": recipientID,
            "sales_id": sales_ids_string,
            "sender_id": sender_id,
            "sentiment": sentiment,
            "chat_id":chat_ids_string,
            "message_text":message_text
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 



#Menampilkan seluruh chat di halaman Contact 
@messageAPI.route('/contact/<string:sales_id>', methods=['GET'])
def contact_get(sales_id):
    try:
        id_checker_sales(sales_id)
        
        # Mengambil seluruh chat pada collection 'chat' yang diurutkan berdasarkan 'last_timestamp' secara descending
        # dan yang memiliki nilai field 'sales_id' sama dengan parameter 'sales_id'
        chat_query = chat_ref.where('sales_id', '==', sales_id).order_by('last_timestamp', direction=firestore.Query.DESCENDING).get()

        contacts = []
        
        for chat in chat_query:
            chat_data = chat.to_dict()
            chat_id = chat.id
            status = chat_data.get('status')
            
            # Menghitung jumlah pesan pada collection 'message' yang memiliki field 'read_status' = False
            # dan 'chat_id' sama dengan chat_id dari iterasi saat ini
            unread_query = message_ref.where('chat_id', '==', chat_id).where('read_status', '==', False).get()
            unread_count = len(unread_query)
            
            # Mengambil data pesan terbaru dari collection 'message' yang memiliki field 'chat_id' sama dengan chat_id dari iterasi saat ini
            message_query = message_ref.where('chat_id', '==', chat_id).order_by('time_stamp', direction=firestore.Query.DESCENDING).limit(1).get()
            
            #membuat variabel waktu saat ini
            current_time = datetime.now()

            for message in message_query:
                message_data = message.to_dict()
                sender_id = message_data.get('sender_id')
                message_id = message.id
                message_text = message_data.get('message_text')
                timestamp = message_data.get('time_stamp')
                # Jika timestamp di hari yang sama dengan waktu server, tampilkan jam
                if timestamp.date() == current_time.date():
                    time = timestamp.strftime("%H:%M")
        
                # Jika timestamp sehari sesudah waktu server, tampilkan "Yesterday"
                elif timestamp.date() == current_time.date() - timedelta(days=1):
                    time = "Yesterday"
                
                # Jika timestamp lebih dari sehari dari waktu server, tampilkan format dd/mm/yy
                else:
                    time = timestamp.strftime("%d/%m/%y")

                contacts.append({
                    'chat_id': chat_id,
                    'status': status,
                    'sender_id': sender_id,
                    'message_id': message_id,
                    'last_message_text': message_text,
                    'time_stamp': time,
                    'unread_count': unread_count
                })
        
        return jsonify(contacts), 200
    
    except Exception as e:
        return jsonify({'message': 'Access Denied', 'error': str(e)}), 401


#Menampilkan chat setiap sender
@messageAPI.route('/chat/<string:chat_id>', methods=['GET'])
def get_messages_by_chat_ids(chat_id):
    
    try:
        #mengupdate status management/chat menjadi ditangani
        chat_ref.document(chat_id).update({'status':'ditangani' })

        
        message_query = message_ref.where('chat_id', '==', chat_id).order_by('time_stamp', direction=firestore.Query.DESCENDING).get()
        all_messages = []
        for message in message_query:
            message_data = message.to_dict()
            # Mengupdate field "read_status" menjadi true
            message.reference.update({'read_status': True})

            all_messages.append(message_data)
        return jsonify(all_messages), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@messageAPI.route('/all', methods=['GET'])
def get_all_messages():
    messages = message_ref.get()
    all_messages = []
    for message in messages:
        message_data = message.to_dict()
        all_messages.append(message_data)

    return jsonify(all_messages), 200
