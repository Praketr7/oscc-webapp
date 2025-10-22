from flask import Flask, request, jsonify, send_file
import joblib
from flask_cors import CORS
from db import get_connection
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load models
model_nstage = joblib.load("rusboost.pkl")
model_ene = joblib.load("catboost.pkl")

sex_mapping = {"M": 1, "F": 2}
EXCEL_PATH = os.path.join(os.getcwd(), "output.xlsx")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    sex_input = sex_mapping.get(data['sex'])

    # Convert inputs
    inputs = [
        int(data["age"]),
        sex_input,
        int(data["sites"]),
        float(data["doi"]),
        int(data["tStage"]),
        float(data["nlr"]),
        float(data["pmr"]),
        float(data["plr"]),
        float(data["lmr"]),
        float(data["sii"])
    ]

    # Make predictions
    prediction_nstage = int(model_nstage.predict([inputs])[0])
    prediction_ene = int(model_ene.predict([inputs])[0])

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Insert only if tuple doesn't exist
        cursor.execute("""
            SELECT 1 FROM oscc_table
            WHERE age=%s AND sex=%s AND sites=%s AND doi=%s AND tstage=%s
              AND nlr=%s AND pmr=%s AND plr=%s AND lmr=%s AND sii=%s
        """, tuple(inputs))

        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO oscc_table
                (age, sex, sites, doi, tstage, nlr, pmr, plr, lmr, sii, nstage, ene)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(inputs + [prediction_nstage, prediction_ene]))
            conn.commit()
            print("✅ Inserted new row in oscc_table.")
        else:
            print("ℹ️ Duplicate detected — no new insert.")

        # Update Excel file after every insert
        try:
            df = pd.read_sql_query("SELECT * FROM oscc_table", conn)
            df.to_excel(EXCEL_PATH, index=False)
            print(f"✅ Excel updated at: {EXCEL_PATH}")
        except Exception as ex:
            print("⚠️ Excel update failed:", ex)

        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ DB Error:", e)
        return jsonify({"error": "Database error"}), 500

    return jsonify({
        "nstage": prediction_nstage,
        "ene": prediction_ene
    })


# New route for downloading the Excel file
@app.route('/download_excel', methods=['GET'])
def download_excel():
    if os.path.exists(EXCEL_PATH):
        return send_file(
            EXCEL_PATH,
            as_attachment=True,
            download_name="oscc_predictions.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        return jsonify({"error": "Excel file not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
