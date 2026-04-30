from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "Backend is working!"

@app.route("/api/analyze-cv", methods=["POST"])
def analyze():
    try:
        data = request.json
        cv = data.get("cv", "")
        job = data.get("job", "")

        return jsonify({
            "result": f"""
ATS Score: 78/100

Missing Keywords:
- MATLAB
- AutoCAD
- Power Electronics

Weak Points:
- No real work experience
- Projects not detailed

Improved Summary:
Motivated Electrical Engineering student with strong foundation in circuit analysis and programming. Seeking to apply technical skills in real-world engineering environments.
"""
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500