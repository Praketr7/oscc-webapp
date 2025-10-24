from flask import Flask, request, jsonify, send_file
import joblib
from flask_cors import CORS
import pandas as pd
import os
import traceback

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
    try:
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

        # Save Excel locally
        df = pd.DataFrame([{
            "age": inputs[0],
            "sex": inputs[1],
            "sites": inputs[2],
            "doi": inputs[3],
            "tstage": inputs[4],
            "nlr": inputs[5],
            "pmr": inputs[6],
            "plr": inputs[7],
            "lmr": inputs[8],
            "sii": inputs[9],
            "nstage": prediction_nstage,
            "ene": prediction_ene
        }])
        df.to_excel(EXCEL_PATH, index=False)

        return jsonify({
            "nstage": prediction_nstage,
            "ene": prediction_ene
        })
    except Exception as e:
        print("❌ Error during prediction:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
