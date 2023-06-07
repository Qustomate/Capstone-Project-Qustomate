# Mengimport library yang dibutuhkan
from flask import Flask, jsonify, request, Blueprint
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

sentimentResultAPI = Blueprint('sentimentResultAPI', __name__) #Membuat blueprint untuk mendefinisikan API sentimentResultAPI
app = Flask(__name__) #Membuat instance untuk menjalankan server
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
        sentiment = 0, 'negative'
    else:
        sentiment = 1, 'positive'
    
    return sentiment

# Endpoint API untuk prediksi sentimen
@sentimentResultAPI.route('/predict_sentiment', methods=['POST'])
def predict_sentiment_api():
    # data = request.json()  # Menerima data teks dari klien
    # text = data['text']
    text = request.json['text']
    # Melakukan prediksi sentimen
    sentiment = predict_sentiment(text)

    # Mengembalikan hasil prediksi sebagai respons JSON
    response = {'sentiment': sentiment}
    return jsonify({'message': 'Melakukan predict', 'sentiment': sentiment})
