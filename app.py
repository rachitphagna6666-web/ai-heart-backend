from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>AI Heart System</title>
</head>
<body>

<h1>Heart Failure Prediction</h1>

<input id="age" placeholder="Age"><br>
<input id="bp" placeholder="BP"><br>
<input id="chol" placeholder="Cholesterol"><br>
<input id="hr" placeholder="Heart Rate"><br>

<button onclick="predict()">Predict</button>

<h2 id="result"></h2>

<script>
async function predict() {
    let res = await fetch('/predict', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            age: Number(document.getElementById('age').value),
            bp: Number(document.getElementById('bp').value),
            chol: Number(document.getElementById('chol').value),
            hr: Number(document.getElementById('hr').value)
        })
    });

    let data = await res.json();

    document.getElementById('result').innerHTML =
        data.risk + " (" + data.probability + "%)";
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    score = (data["age"] * 0.2) + (data["bp"] * 0.25) + (data["chol"] * 0.25) - (data["hr"] * 0.15)
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

if __name__ == "__main__":
    app.run()
