from flask import Flask, request, jsonify
import joblib
from flask_cors import CORS
from db import get_connection

app = Flask(__name__)
CORS(app)
model_nstage = joblib.load("rusboost.pkl")
model_ene = joblib.load("catboost.pkl")

model = joblib.load("rusboost.pkl")
sex_mapping = {"M": 1, "F": 2}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    sex_input = sex_mapping.get(data['sex'])

    age = int(data["age"])
    sex = sex_input
    sites = int(data["sites"])
    doi = float(data["doi"])
    tStage = int(data["tStage"])
    nlr = float(data["nlr"])
    pmr = float(data["pmr"])
    plr = float(data["plr"])
    lmr = float(data["lmr"])
    sii = float(data["sii"])

    inputs = [
        data["age"], sex_input, data["sites"], data["doi"],
        data["tStage"], data["nlr"], data["pmr"], data["plr"],
        data["lmr"], data["sii"]
    ]

    prediction_nstage = model_nstage.predict([inputs])
    prediction_ene = model_ene.predict([inputs])
    return jsonify({'nstage': int(prediction_nstage[0]), "ene": int(prediction_ene[0])})
    
    nstage = int(predictions[0])
    

    # Save to DB, avoid duplicate tuples
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if exact tuple exists
        cursor.execute("""
            SELECT 1 FROM oscc_table
            WHERE age=%s AND sex=%s AND sites=%s AND doi=%s AND tstage=%s
              AND nlr=%s AND pmr=%s AND plr=%s AND lmr=%s AND sii=%s
        """, (
            data["age"], sex_input, data["sites"], data["doi"], data["tStage"],
            data["nlr"], data["pmr"], data["plr"], data["lmr"], data["sii"]
        ))

        if cursor.fetchone() is None:
            # Insert if not exists
            cursor.execute("""
                INSERT INTO oscc_table
                (age, sex, sites, doi, tstage, nlr, pmr, plr, lmr, sii, nstage)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data["age"], sex_input, data["sites"], data["doi"], data["tStage"],
                data["nlr"], data["pmr"], data["plr"], data["lmr"], data["sii"], nstage
            ))
            conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:
        print("DB Error:", e)
        return jsonify({"error": "Database error"}), 500

    return jsonify({"prediction": nstage})

if __name__ == '__main__':
    app.run(debug=True)
