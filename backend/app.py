import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)

# Load models
model_nstage = joblib.load("rusboost.pkl")
model_ene = joblib.load("catboost.pkl")

sex_mapping = {"M": 1, "F": 2}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    print("📝 Received JSON:", data)  # Debug: show incoming request

    try:
        sex_input = sex_mapping.get(data.get("sex"))
        print("🔹 Mapped sex:", sex_input)  # Debug

        inputs = [
            int(data.get("age", 0)),
            sex_input,
            int(data.get("sites", 0)),
            float(data.get("doi", 0.0)),
            int(data.get("tStage", 0)),
            float(data.get("nlr", 0.0)),
            float(data.get("pmr", 0.0)),
            float(data.get("plr", 0.0)),
            float(data.get("lmr", 0.0)),
            float(data.get("sii", 0.0))
        ]
        print("🔹 Model input list:", inputs)  # Debug

        # Make predictions
        prediction_nstage = int(model_nstage.predict([inputs])[0])
        prediction_ene = int(model_ene.predict([inputs])[0])

        print("✅ Predictions:", {"nstage": prediction_nstage, "ene": prediction_ene})  # Debug

        return jsonify({
            "nstage": prediction_nstage,
            "ene": prediction_ene
        })

    except Exception as e:
        print("❌ Error during prediction:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = 10000
    print(f"🚀 Starting Flask app on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
