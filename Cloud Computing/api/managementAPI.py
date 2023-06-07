from flask import Blueprint, jsonify, request
from firebase_admin import firestore


managementAPI = Blueprint('managementAPI', __name__)


from .function import id_checker_sales,id_checker_chat, sales_ref, chat_ref, message_ref ,id_checker_message,generate_rdm_id, db

    
@managementAPI.route('/list/<string:sales_id>',methods=['GET'])
def list_management(sales_id):
    try:
        id_checker_sales(sales_id)
        
        #Query untuk mengambil data chat yang berkondisi terakhir chat paing baru
        chat_query = chat_ref.where('sales_id', '==', sales_id).order_by('last_timestamp', direction=firestore.Query.DESCENDING).get()

        management = []
        
        for chat in chat_query:
            chat_data = chat.to_dict()
            chat_id = chat.id
            name = chat_data.get('name')
            status = chat_data.get('status')
            produk = chat_data.get('produk')
            sender_id = chat_data.get('sender_id')
            revenue = chat_data.get('revenue')
            mulai_chat=chat_data.get('first_timestamp')
            terakhir_chat=chat_data.get('last_timestamp')
            alamat = chat_data.get('alamat')
            kota = chat_data.get('kota')
            catatan = chat_data.get('catatan')
            new_message = chat_data.get('new_message_count')


            #wadah untuk menambahkan data chat sehingga dapat diurutkan
            management.append({
                    'chat_id': chat_id,
                    'name': name,
                    'status': status,
                    'produk':produk,
                    'revenue':revenue,
                    'mulai_chat':mulai_chat,
                    'terakhir_chat':terakhir_chat,
                    'alamat':alamat,
                    'kota':kota,
                    'catatan':catatan,
                    'new_message':new_message                    
                })

        return jsonify({'message':'connected'},management), 200
    except Exception as e:
        return jsonify({'message': 'Access Denied', 'error': str(e)}), 401





#menyimpan perubaahan pada Edit Management
@managementAPI.route('/save/<string:sales_id>/<string:chat_id>', methods=['PUT'])
def save_chat(sales_id,chat_id):
    try:
        id_checker_sales(sales_id)
        id_checker_chat(chat_id)
        chat_doc= chat_ref.document(chat_id)

        data = request.get_json()
        status = data.get('status')
        name = data.get('name')
        produk = data.get('produk')
        revenue = data.get('revenue')
        alamat =data.get('alamat')
        kota = data.get('kota')
        catatan=data.get('catatan')

        chat_doc.update({
            'status': status,
            'name': name,
            'produk': produk,
            'revenue': revenue,
            'alamat': alamat,
            'kota': kota,
            'catatan': catatan
        })

        return jsonify({'message':'Udate Success'}), 200
    except Exception as e:
        return jsonify({'message': 'Access Denied', 'error': str(e)}), 401

#mengambil data yang lama pada edit chat
@managementAPI.route('/edit/<string:sales_id>/<string:chat_id>', methods=['GET'])
def edit_chat(sales_id,chat_id):
    try:
        
        id_checker_sales(sales_id)
        id_checker_chat(chat_id)

        query = chat_ref.where('chat_id', '==', chat_id).get()
        chat_data = query[0].to_dict()

        status = chat_data['status']
        name = chat_data['name']
        # nomor_hp = chat_data['nomor_hp']
        produk = chat_data['produk']
        revenue = chat_data['revenue']    
        alamat = chat_data['alamat']
        kota = chat_data['kota']
        catatan = chat_data['catatan']
         
        return jsonify({
                'status':status,
                'name':name,
                'produk':produk,
                'revenue':revenue,
                'alamat':alamat,
                'kota':kota,
                'catatan':catatan

            },{'message':'Get data Success'}), 200
    except Exception as e:
        return jsonify({'message': 'Access Denied', 'error': str(e)}), 401
