from flask import Flask, jsonify, request, Blueprint
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

sentimentResultAPI = Blueprint('sentimentResultAPI', __name__)
app = Flask(__name__)
model = load_model('api/qustomate(v4)-model.h5')
tokenizer = Tokenizer()

# Fungsi untuk melakukan prediksi sentimen
def predict_sentiment(text):
    # Preprocessing teks
    text = [text]
    tokenizer.fit_on_texts(text)
    text = tokenizer.texts_to_sequences(text)
    text = pad_sequences(text, maxlen=360)

    # Melakukan prediksi sentimen
    prediction = model.predict(text)[0][0]

    # Mengembalikan hasil prediksi
    ambang_batas = 0.5
    if prediction <= ambang_batas:
        sentiment = 0, 'positive'
    else:
        sentiment = 1, 'negative'
    
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
    return jsonify({'message': 'Predict berhasil', 'sentiment': sentiment})