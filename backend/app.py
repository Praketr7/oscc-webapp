from flask import Flask, request, jsonify
import joblib
from flask_cors import CORS
from db import get_connection


app = Flask(__name__)
CORS(app)

model = joblib.load("rusboost.pkl")
sex_mapping = {"Male":1, "Female":2}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    sex_input = sex_mapping.get(data['sex'])
    inputs = [data["age"], sex_input, data["sites"], data["doi"], data["tStage"], data["nlr"], data["pmr"], data["plr"], data["lmr"], data["sii"]]
    
    # Make prediction
    predictions = model.predict([inputs])
    nstage = int(predictions[0])
    
    # Save to DB
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO oscc_table(age, sex, sites, doi, tstage, nlr, pmr, plr, lmr, sii, nstage)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (data["age"], sex_input, data["sites"], data["doi"], data["tStage"], data["nlr"], data["pmr"], data["plr"], data["lmr"], data["sii"], nstage)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("DB Error:", e)

    return jsonify({'prediction': nstage})

if __name__=='__main__':
    app.run(debug=True)
