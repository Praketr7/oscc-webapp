from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load("rusboost.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    