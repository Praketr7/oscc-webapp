"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Label } from "./ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select"

export default function PredictionForm({ onPredict, loading }) {
  const [formData, setFormData] = useState({
    age: "",
    sex: "",
    sites: "",
    doi: "",
    tStage: "",
    nlr: "",
    pmr: "",
    plr: "",
    lmr: "",
    sii: "",
  })

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()

    // Validate all fields are filled
    if (Object.values(formData).some((v) => v === "")) {
      alert("Please fill in all fields")
      return
    }

    onPredict(formData)
  }

  const isFormValid = Object.values(formData).every((v) => v !== "")

  return (
    <Card className="border-2 border-teal-200 shadow-lg bg-white">
      <CardHeader className="bg-gradient-to-r from-blue-50 to-teal-50 border-b-2 border-teal-200">
        <CardTitle className="text-teal-900 pt-3">Clinical Parameters</CardTitle>
        <CardDescription className="text-teal-700 pb-3">Enter patient clinical data for prediction</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Demographics */}
          <div className="space-y-4 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
            <h3 className="font-semibold text-blue-900">Demographics</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="age" className="text-sm font-medium text-blue-900">
                  Age (years)
                </Label>
                <Input
                  id="age"
                  type="number"
                  min="18"
                  max="120"
                  placeholder="45"
                  value={formData.age}
                  onChange={(e) => handleInputChange("age", e.target.value)}
                  className="border-blue-300 focus:border-blue-500 focus:ring-blue-500"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="sex" className="text-sm font-medium text-blue-900">
                  Sex
                </Label>
                <Select value={formData.sex} onValueChange={(v) => handleInputChange("sex", v)}>
                  <SelectTrigger className="border-blue-300 focus:border-blue-500">
                    <SelectValue placeholder="Select" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="M">Male</SelectItem>
                    <SelectItem value="F">Female</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>

          {/* Tumor Characteristics */}
          <div className="space-y-4 p-4 bg-teal-50 rounded-lg border-l-4 border-teal-500">
            <h3 className="font-semibold text-teal-900">Tumor Characteristics</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="sites" className="text-sm font-medium text-teal-900">
                  Sites
                </Label>
                <Input
                  id="sites"
                  type="number"
                  min="1"
                  max="3"
                  placeholder="2"
                  value={formData.sites}
                  onChange={(e)=>handleInputChange("sites", e.target.value)}
                  className="border-blue-300 focus:border-blue-500 focus:ring-blue-500"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="doi" className="text-sm font-medium text-teal-900">
                  DOI (mm)
                </Label>
                <Input
                  id="doi"
                  type="number"
                  min="0"
                  step="0.1"
                  placeholder="8.5"
                  value={formData.doi}
                  onChange={(e) => handleInputChange("doi", e.target.value)}
                  className="border-teal-300 focus:border-teal-500 focus:ring-teal-500"
                />
              </div>
            </div>
            <div className="grid grid-cols-5 gap-4">
              <div className="space-y-2 col-span-2">
                <Label htmlFor="tStage" className="text-sm font-medium text-teal-900">
                  T Stage
                </Label>
                <Input
                  id="tStage"
                  type="number"
                  min="1"
                  max="4"
                  placeholder="3"
                  value={formData.tStage}
                  onChange={(e)=>handleInputChange("tStage", e.target.value)}
                  className="border-teal-300 focus:border-teal-500 focus:ring-teal-500"
                />
              </div>
            </div>
          </div>

          {/* Immune Markers */}
          <div className="space-y-4 p-4 bg-cyan-50 rounded-lg border-l-4 border-cyan-500">
            <h3 className="font-semibold text-cyan-900">Immune Markers</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="nlr" className="text-sm font-medium text-cyan-900">
                  NLR
                </Label>
                <Input
                  id="nlr"
                  type="number"
                  min="0"
                  step="0.1"
                  placeholder="2.5"
                  value={formData.nlr}
                  onChange={(e) => handleInputChange("nlr", e.target.value)}
                  className="border-cyan-300 focus:border-cyan-500 focus:ring-cyan-500"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="pmr" className="text-sm font-medium text-cyan-900">
                  PMR
                </Label>
                <Input
                  id="pmr"
                  type="number"
                  min="0"
                  step="0.1"
                  placeholder="85"
                  value={formData.pmr}
                  onChange={(e) => handleInputChange("pmr", e.target.value)}
                  className="border-cyan-300 focus:border-cyan-500 focus:ring-cyan-500"
                />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="plr" className="text-sm font-medium text-cyan-900">
                  PLR
                </Label>
                <Input
                  id="plr"
                  type="number"
                  min="0"
                  step="0.1"
                  placeholder="120"
                  value={formData.plr}
                  onChange={(e) => handleInputChange("plr", e.target.value)}
                  className="border-cyan-300 focus:border-cyan-500 focus:ring-cyan-500"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="lmr" className="text-sm font-medium text-cyan-900">
                  LMR
                </Label>
                <Input
                  id="lmr"
                  type="number"
                  min="0"
                  step="0.1"
                  placeholder="4.2"
                  value={formData.lmr}
                  onChange={(e) => handleInputChange("lmr", e.target.value)}
                  className="border-cyan-300 focus:border-cyan-500 focus:ring-cyan-500"
                />
              </div>
            </div>
            <div className="grid grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="sii" className="text-sm font-medium text-cyan-900">
                  SII
                </Label>
                <Input
                  id="sii"
                  type="number"
                  min="0"
                  step="1"
                  placeholder="450"
                  value={formData.sii}
                  onChange={(e) => handleInputChange("sii", e.target.value)}
                  className="border-cyan-300 focus:border-cyan-500 focus:ring-cyan-500"
                />
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <Button
            type="submit"
            disabled={!isFormValid || loading}
            className="w-full bg-gradient-to-r from-blue-600 to-teal-600 hover:from-blue-700 hover:to-teal-700 text-white font-semibold shadow-md"
          >
            {loading ? "Predicting..." : "Predict N Stage & ENE"}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
