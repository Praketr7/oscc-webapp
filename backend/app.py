@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    try:
        # Map sex to numeric
        sex_input = sex_mapping.get(data["sex"])

        # DB input dict
        db_inputs = {
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

        # Define feature names manually (must match the order used when training the models)
        feature_names = ["age", "sex", "sites", "doi", "tstage", "nlr", "pmr", "plr", "lmr", "sii"]

        # Create DataFrames for prediction
        nstage_input_df = pd.DataFrame([list(db_inputs.values())], columns=feature_names)
        ene_input_df = pd.DataFrame([list(db_inputs.values())], columns=feature_names)

        # Make predictions
        db_inputs["nstage"] = int(model_nstage.predict(nstage_input_df)[0])
        db_inputs["ene"] = int(model_ene.predict(ene_input_df)[0])

        # Insert into Supabase if not exists
        insert_if_not_exists(db_inputs)

        # Update Excel
        df_res = requests.get(f"{SUPABASE_URL}/rest/v1/oscc_table", headers=HEADERS).json()
        if df_res:
            df = pd.DataFrame(df_res)
            df.to_excel(EXCEL_PATH, index=False)

        return jsonify({"nstage": db_inputs["nstage"], "ene": db_inputs["ene"]})

    except Exception as e:
        print("❌ Prediction / Supabase error:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
