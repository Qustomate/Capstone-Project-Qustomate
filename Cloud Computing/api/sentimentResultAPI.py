# Mengimport library yang dibutuhkan
from flask import Flask, jsonify, request, Blueprint
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

model = load_model('api/sentiment_model_qustomate_v4.h5') #Memuat model yang telah dilatih
tokenizer = Tokenizer() #Digunakan untuk pre-processing teks

# Fungsi untuk melakukan prediksi sentimen
def predict_sentiment(text):
    # Preprocessing teks
    #text = [text]
    tokenizer.fit_on_texts(text)
    text = tokenizer.texts_to_sequences(text)
    text = pad_sequences(text, maxlen=360)

    # Melakukan prediksi sentimen
    prediction = model.predict(text)[0][0]

    # Mengembalikan hasil prediksi
    threshold = 0.6
    if prediction < threshold:
        sentiment = 0
    else:
        sentiment = 1
    
    return sentiment

