from flask import Flask, request, jsonify
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
model = joblib.load("rusboost.pkl")

sex_mapping = {"Male":1, "Female":2}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    sex_input = sex_mapping.get(data['sex'])
    inputs = [data["age"], sex_input, data["sites"], data["doi"], data["tStage"], data["nlr"], data["pmr"], data["plr"], data["lmr"], data["sii"]]
    predictions = model.predict([inputs])
    return jsonify({'prediction': int(predictions[0])})

if __name__=='__main__':
    app.run(debug=True)