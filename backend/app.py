from flask import Flask, request, jsonify
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
model_nstage = joblib.load("rusboost.pkl")
model_ene = joblib.load("catboost.pkl")

sex_mapping = {"Male":1, "Female":2}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    sex_input = sex_mapping.get(data['sex'])
    inputs = [data["age"], sex_input, data["sites"], data["doi"], data["tStage"], data["nlr"], data["pmr"], data["plr"], data["lmr"], data["sii"]]
    prediction_nstage = model_nstage.predict([inputs])
    prediction_ene = model_ene.predict([inputs])
    return jsonify({'nstage': int(prediction_nstage[0]), "ene": int(prediction_ene[0])})

if __name__=='__main__':
    app.run(debug=True)