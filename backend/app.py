import os
import requests
import joblib
import pandas as pd
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL").rstrip("/")  # Remove trailing slash if any
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# Paths & models
EXCEL_PATH = os.path.join(os.getcwd(), "output.xlsx")
model_nstage = joblib.load("rusboost.pkl")
model_ene = joblib.load("catboost.pkl")
sex_mapping = {"M": 1, "F": 2}


def insert_if_not_exists(data_dict):
    """
    Checks if a row exists in Supabase; inserts if it doesn't.
    Ignores predicted columns when checking for duplicates.
    """
    filter_parts = [f"{k}=eq.{v}" for k, v in data_dict.items() if k not in ["nstage", "ene"]]
    query = "&".join(filter_parts)
    url = f"{SUPABASE_URL}/rest/v1/oscc_table?{query}"

    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print("❌ Supabase GET failed:", res.status_code, res.text)
        return False

    if len(res.json()) == 0:
        r = requests.post(f"{SUPABASE_URL}/rest/v1/oscc_table", headers=HEADERS, json=data_dict)
        if r.status_code not in (200, 201):
            print("❌ Supabase POST failed:", r.status_code, r.text)
        return r.status_code in (200, 201)

    return False


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

        # Predictions
        inputs["nstage"] = int(model_nstage.predict([list(inputs.values())])[0])
        inputs["ene"] = int(model_ene.predict([list(inputs.values())])[0])

        # Insert into Supabase if new
        insert_if_not_exists(inputs)

        # Update Excel from Supabase
        df_res = requests.get(f"{SUPABASE_URL}/rest/v1/oscc_table", headers=HEADERS).json()
        if df_res:
            df = pd.DataFrame(df_res)
            df.to_excel(EXCEL_PATH, index=False)

        return jsonify({"nstage": inputs["nstage"], "ene": inputs["ene"]})

    except Exception as e:
        print("❌ Prediction / Supabase error:", e)
        return jsonify({"error": "Internal server error"}), 500


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


@app.route("/test_supabase")
def test_supabase():
    url = f"{SUPABASE_URL}/rest/v1/oscc_table"
    r = requests.get(url, headers=HEADERS)
    return jsonify({
        "status": r.status_code,
        "response": r.text
    })


if __name__ == "__main__":
    # Render assigns a dynamic port; default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
