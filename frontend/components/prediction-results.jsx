"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"

export default function PredictionResults({ predictions }) {
  const getNStageColor = (stage) => {
    switch (stage) {
      case "N0":
        return "bg-green-50 border-green-300"
      case "N1":
        return "bg-yellow-50 border-yellow-300"
      case "N2":
        return "bg-orange-50 border-orange-300"
      case "N3":
        return "bg-red-50 border-red-300"
      default:
        return "bg-slate-50 border-slate-200"
    }
  }
  
  const getENEColor = (risk) => {
    switch (risk) {
      case "Low":
        return "bg-green-50 border-green-300"
      case "Moderate":
        return "bg-yellow-50 border-yellow-300"
      case "High":
        return "bg-red-50 border-red-300"
      default:
        return "bg-slate-50 border-slate-200"
    }
  }

  const getNStageTextColor = (stage) => {
    switch (stage) {
      case "N0":
        return "text-green-700"
      case "N1":
        return "text-yellow-700"
      case "N2":
        return "text-orange-700"
      case "N3":
        return "text-red-700"
      default:
        return "text-slate-700"
    }
  }

  const getENETextColor = (risk) => {
    switch (risk) {
      case "Low":
        return "text-green-700"
      case "Moderate":
        return "text-yellow-700"
      case "High":
        return "text-red-700"
      default:
        return "text-slate-700"
    }
  }

  return (
    <Card className="border-2 border-teal-200 shadow-lg bg-white">
      <CardHeader className="bg-gradient-to-r from-blue-50 to-teal-50 border-b-2 border-teal-200">
        <CardTitle className="text-teal-900 pt-3">Prediction Results</CardTitle>
        <CardDescription className="text-teal-700 pb-3">Model predictions based on input parameters</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4 pt-6">
        {/* N Stage */}
        <div className={`p-4 rounded-lg border-2 ${getNStageColor(predictions.nStage)} shadow-sm`}>
          <p className="text-sm font-medium text-slate-600 mb-1">Predicted N Stage</p>
          <p className={`text-3xl font-bold ${getNStageTextColor(predictions.nStage)}`}>{predictions.nStage}</p>
        </div>

        {/* ENE Risk */}
        <div className={`p-4 rounded-lg border-2 ${getENEColor(predictions.eneRisk)} shadow-sm`}>
          <p className="text-sm font-medium text-slate-600 mb-1">ENE Risk Level</p>
          <p className={`text-3xl font-bold ${getENETextColor(predictions.eneRisk)}`}>{predictions.eneRisk}</p>
        </div>

        {/* Confidence */}
        <div className="p-4 rounded-lg border-2 border-blue-300 bg-blue-50 shadow-sm">
          <p className="text-sm font-medium text-slate-600 mb-2">Model Confidence</p>
          <div className="flex items-center gap-2">
            <div className="flex-1 bg-slate-200 rounded-full h-2">
              <div
                className="bg-gradient-to-r from-blue-500 to-teal-500 h-2 rounded-full transition-all"
                style={{ width: `${predictions.confidence}%` }}
              />
            </div>
            <span className="text-lg font-semibold text-blue-700">{predictions.confidence}%</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
