from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "AI Heart API Running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    age = data["age"]
    bp = data["bp"]
    chol = data["chol"]
    hr = data["hr"]

    score = (age * 0.2) + (bp * 0.25) + (chol * 0.25) - (hr * 0.15)
    risk = max(0, min((score / 300) * 100, 100))

    if risk < 30:
        level = "Low Risk"
    elif risk < 60:
        level = "Moderate Risk"
    else:
        level = "High Risk"

    return jsonify({
        "risk": level,
        "probability": round(risk, 2)
    })
