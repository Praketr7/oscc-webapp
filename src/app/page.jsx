"use client";

import { useState } from "react";
import PredictionForm from "../components/prediction-form"

export default function Page() {
  const [result, setResult] = useState({nstage:"", ene:""});
  const [loading, setLoading] = useState(false);

  const handlePredict = async (formData) => {
    setLoading(true);
    setResult({nstage:"", ene:""}); //
    try {
      const res = await fetch("https://oscc-webapp.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      const displayResult = {
        nstage: data.nstage === 0 ? "N-" : "N+",
        ene: data.ene === 0? "Negative" : "Positive", 
      };
      setResult(displayResult);
    } catch (err) {
      console.error(err);
      alert("Prediction failed!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <PredictionForm onPredict={handlePredict} loading={loading} />
      {(result.ene || result.nstage) && (
        <div>
          <div className="mt-8 p-4 bg-gradient-to-r from-blue-400 to-teal-600 text-white rounded-md font-semibold">
            Predicted N Stage: {result.nstage}
          </div>
          <div className="mt-2 p-4 bg-gradient-to-r from-blue-400 to-teal-600 text-white rounded-md font-semibold">
            Predicted ENE: {result.ene}              
          </div>
        </div>
      )}
    </div>
  );
}
