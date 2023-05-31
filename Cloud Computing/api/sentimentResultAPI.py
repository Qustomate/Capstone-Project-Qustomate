from flask import Blueprint, jsonify, request
from firebase_admin import firestore

db = firestore.client()
sentimentResultAPI = Blueprint('sentimentResultAPI', __name__)

# @sentimentResultAPI.route('/doing', methods=['GET'])
# def get_all_messages():
#     messages_ref = db.collection('message')
#     messages = messages_ref.get()

#     all_messages = []
#     for message in messages:
#         message_data = message.to_dict()
#         all_messages.append(message_data)

#     return jsonify(all_messages), 200