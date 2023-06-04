from flask import Blueprint, jsonify, request
from firebase_admin import firestore

db = firestore.client()
managementAPI = Blueprint('managementAPI', __name__)
sales_ref = db.collection('sales')
chat_ref = db.collection('chat')    
def id_checker(sales_id,chat_id):
    sales_id_query = sales_ref.where('sales_id', '==', sales_id).get()
    chat_id_query = chat_ref.where('chat_id', '==', chat_id).get()
    if not sales_id_query:
        raise ValueError(f'Sales account id :{sales_id} tidak ditemukan')
    if not chat_id_query:
        raise ValueError(f'Chat id : {chat_id} tidak ditemukan')
    

@managementAPI.route('/save/<string:sales_id>/<string:chat_id>', methods=['PUT'])
def save_chat(sales_id,chat_id):
    try:
        id_checker(sales_id,chat_id)
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

@managementAPI.route('/edit/<string:sales_id>/<string:chat_id>', methods=['GET'])
def edit_chat(sales_id,chat_id):
    try:
        query = chat_ref.where('chat_id', '==', chat_id).get()
        id_checker(sales_id,chat_id)
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