from flask import Blueprint, jsonify, request
from firebase_admin import firestore
from .function import id_checker_sales, sales_ref, chat_ref, message_ref 

DashboardAPI = Blueprint('DashboardAPI', __name__)




@DashboardAPI.route('/<string:sales_id>', methods=['GET'])
def done_status(sales_id):
    status_list = ['baru', 'ditangani', 'selesai', 'batal']
    chat_counts = {}
    total_revenue = 0
    persentage_positif=0
    persentage_negatif=0
    
    try :             
        id_checker_sales(sales_id)
        query = sales_ref.where('sales_id', '==', sales_id).get()
        sales_data = query[0].to_dict()
        client_handler = sales_data['client_handler']             
                
        for status in status_list:
            chat_query = chat_ref.where('sales_id', '==', sales_id).where('status', '==', status).get()
            chat_counts[status] = len(chat_query)
        
        revenue_query = chat_ref.where('sales_id', '==', sales_id).where('status', '==', 'selesai').get()
        for doc in revenue_query:
            chat_data = doc.to_dict()
            revenue = chat_data.get('revenue', 0)
            total_revenue += revenue        

        positive_query = message_ref.where('sales_id', '==', sales_id).where('sentiment', '==', 'positive').get()
        negative_query = message_ref.where('sales_id', '==', sales_id).where('sentiment', '==', 'negative').get()

        first_name = sales_data['firstname']
        last_name = sales_data['lastname']
        client_handler = sales_data['client_handler']      
        status_baru = chat_counts['baru']
        status_ditangani = chat_counts['ditangani']
        status_selesai= chat_counts['selesai']
        status_batal = chat_counts['batal']
        positive_count = len(positive_query)
        negative_count = len(negative_query) 
        chat_selesai = chat_counts['selesai']
        if revenue_query:
            persentage_positif= int((positive_count/(len(positive_query)+len(negative_query)))*100)
            persentage_negatif= int((negative_count/(len(positive_query)+len(negative_query)))*100)
        return jsonify({
            'firstname': first_name,
            'lastname': last_name,
            'client_handler': client_handler,
            'status_baru':status_baru,
            'status_ditangani':status_ditangani,
            'status_selesai':status_selesai,
            'status_batal':status_batal,
            'chat_selesai': chat_selesai,
            'persentage_positif': persentage_positif,
            'persentage_negatif': persentage_negatif,
            'total_revenue': total_revenue
        },
        {

            'positive_count':positive_count,
            'negative_count':negative_count,
            'count message': len(positive_query)+len(negative_query),

        }), 200
    except Exception as e:
        return jsonify({'message': 'Access Denide', 'error': str(e)}), 401
        

