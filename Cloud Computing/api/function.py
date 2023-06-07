"""
File ini digunakan sebagai wadah fungsi fungsi yang berulang pada penggunaan enpointnya
"""
from flask import Blueprint, jsonify, request
from firebase_admin import firestore
from datetime import datetime
import uuid

db = firestore.client() #fungsi memanggil database firestore
sales_ref = db.collection('sales')
message_ref = db.collection('message')
chat_ref = db.collection('chat')
admin_ref = db.collection('admin') 
#Membuat sebuah fungsi untuk mempermudah perintah check sales_id 
def id_checker_sales(id):
    #query untuk memanggil data sales bedasarkan id yang diinput pada colletion sales
    id_query = sales_ref.where('sales_id', '==', id).get()
    #jika id tidak ada di colletion
    if not id_query:
       raise ValueError(f'Sales account id :{id} Tidak Ditemukan!')
#Membuat sebuah fungsi untuk mempermudah perintah check chat_id 
def id_checker_chat(id):
    id_query = chat_ref.where('chat_id', '==', id).get()
    if not id_query:
        raise ValueError(f'Chat id : {id} tidak ditemukan')
    
#Membuat sebuah fungsi untuk mempermudah perintah check message_id 
def id_checker_message(id) :
    #query untuk memanggil id pesan agar memastikan tidak ada pesan yg memiliki id sama
    id_query = message_ref.where('id_message', '==', id).get()
    if id_query:
        raise ValueError(f'id_message :{id} Sudah Ada!')

#mengenerate id random untuk penggunaan id acak
def generate_rdm_id(name):
    #selagi dia sama dia akan mengenerete id baru hingga tidak ada yang sama 
    #pada database dengan break
    while True:
        random_number = str(uuid.uuid4())[:15] #menggunakan librari uuid membuat nilai random
        id = name + random_number   #digabung untuk nama penggunaan idnya
        if not chat_ref.document(id).get().exists:
            break                      
    return id
