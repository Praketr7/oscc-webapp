import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)

EXCEL_PATH = os.path.join(os.getcwd(), "output.xlsx")

model_nstage = joblib.load("rusboost.pkl")
model_ene = joblib.load("catboost.pkl")

sex_mapping = {"M": 1, "F": 2}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    try:
        sex_input = sex_mapping.get(data["sex"])
        inputs = {
            "age": int(data["age"]),
            "sex": sex_input,
            "sites": int(data["sites"]),
            "doi": float(data["doi"]),
            "tstage": int(data["tStage"]),
            "nlr": float(data["nlr"]),
            "pmr": float(data["pmr"]),
            "plr": float(data["plr"]),
            "lmr": float(data["lmr"]),
            "sii": float(data["sii"])
        }
        feature_names = ["age", "sex", "sites", "doi", "tstage", "nlr", "pmr", "plr", "lmr", "sii"]
        input_df = pd.DataFrame([list(inputs.values())], columns=feature_names)

        inputs["nstage"] = int(model_nstage.predict(input_df)[0])
        inputs["ene"] = int(model_ene.predict(input_df)[0])

        # Save Excel locally
        df = pd.DataFrame([inputs])
        df.to_excel(EXCEL_PATH, index=False)

        return jsonify({"nstage": inputs["nstage"], "ene": inputs["ene"]})
    except Exception as e:
        print("Error:", e)
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
    return jsonify({"error": "Excel file not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
