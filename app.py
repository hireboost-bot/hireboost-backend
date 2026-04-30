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
    data = request.json
    cv = data.get("cv")
    job = data.get("job")

    prompt = f"""
Analyze CV vs Job.

Give:
- ATS score
- missing keywords
- weak points
- improved summary

CV:
{cv}

JOB:
{job}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return jsonify({"result": res.choices[0].message.content})

app.run()