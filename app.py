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
def analyze_cv():
    try:
        data = request.json or {}
        cv = data.get("cv", "")
        job = data.get("job", "")

        if not cv or not job:
            return jsonify({"error": "CV and job description are required"}), 400

        prompt = f"""
You are an expert ATS resume reviewer.

Analyze this CV against this job description.

Return a clear result with:
1. ATS Score /100
2. Missing Keywords
3. Weak Points
4. Improved Summary
5. Recommended Skills
6. Improved Bullet Points

CV:
{cv}

Job Description:
{job}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        result = response.choices[0].message.content

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500