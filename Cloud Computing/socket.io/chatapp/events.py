from flask import request, Blueprint, jsonify
from flask_socketio import emit

from .extensions import socketio
from firebase_admin import firestore

events = Blueprint("events", __name__)

db = firestore.Client.from_service_account_json("chatapp/serviceAccountKey.json")

users = {}

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    users[username] = request.sid

@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    username = None 
    for user, sid in users.items():
        if sid == request.sid:
            username = user

    # Dapatkan jumlah pesan saat ini
    messages_count = db.collection("chat_messages").document("messages_count")
    doc = messages_count.get()
    current_count = doc.get("count") if doc.exists else 0

    # Simpan data ke Firestore
    doc_ref = db.collection("chat_messages").document(str(current_count + 1))
    doc_ref.set({
        "id": current_count + 1,
        "username": username,
        "message": message
    })

    # Update jumlah pesan saat ini
    messages_count.set({"count": current_count + 1})
    
    emit("chat", {"message": message, "username": username}, broadcast=True)

@events.route("/getmessages/<username>", methods=["GET"])
def get_messages(username):
    # Buat list kosong untuk menyimpan data pesan
    messages = []

    # Ambil semua dokumen dari koleksi "chat_messages"
    docs = db.collection("chat_messages").where("username", "==", username).stream()

    # Loop melalui setiap dokumen dan tambahkan ke list pesan
    for doc in docs:
        message = doc.to_dict()
        messages.append(message)

    # Kirim data pesan sebagai respons JSON
    return jsonify(messages)
