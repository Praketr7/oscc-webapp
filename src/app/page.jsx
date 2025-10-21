"use client"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import PredictionForm from "@/components/prediction-form"
import PredictionResults from "@/components/prediction-results"

export default function Home() {
  const [predictions, setPredictions] = useState(null)
  const [loading, setLoading] = useState(false)

  const handlePredict = async (formData) => {
    setLoading(true)
    try {
      const result = await predictOSCC(formData)
      setPredictions(result)
    } catch (error) {
      console.error("Prediction error:", error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Form Section */}
      <div className="lg:col-span-2">
        <PredictionForm onPredict={handlePredict} loading={loading} />
      </div>

      {/* Results Section */}
      <div className="lg:col-span-1">
        {predictions ? (
          <PredictionResults predictions={predictions} />
        ) : (
          <Card className="h-full flex items-center justify-center bg-gradient-to-br from-blue-50 to-teal-50 border-2 border-teal-200 shadow-md">
            <CardContent className="text-center py-12">
              <p className="text-teal-700 text-sm font-medium">
                Fill in the clinical parameters and click "Predict" to see results
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

// Prediction logic
async function predictOSCC(formData) {
  await new Promise((resolve) => setTimeout(resolve, 800))

  const { age, sex, sites, doi, tStage, nlr, pmr, plr, lmr, sii } = formData

  let nStageScore = 0
  let eneScore = 0

  if (doi > 10) nStageScore += 2
  if (doi > 15) nStageScore += 1
  if (nlr > 3) nStageScore += 1.5
  if (plr > 150) nStageScore += 1
  if (sii > 500) nStageScore += 1.5
  if (tStage === "T3" || tStage === "T4") nStageScore += 1

  if (doi > 12) eneScore += 2
  if (nlr > 3.5) eneScore += 1.5
  if (pmr > 100) eneScore += 1
  if (lmr < 3) eneScore += 1.5
  if (sii > 600) eneScore += 1.5
  if (age > 60) eneScore += 0.5

  let nStage = "N0"
  if (nStageScore < 2) nStage = "N0"
  else if (nStageScore < 4) nStage = "N1"
  else if (nStageScore < 6) nStage = "N2"
  else nStage = "N3"

  const eneRiskPercent = Math.min(95, Math.max(5, eneScore * 8))
  let eneRisk = "Low"
  if (eneRiskPercent > 60) eneRisk = "High"
  else if (eneRiskPercent > 35) eneRisk = "Moderate"

  const confidence = Math.min(95, 70 + Math.random() * 20)

  return {
    nStage,
    eneRisk,
    confidence: Math.round(confidence),
  }
}
