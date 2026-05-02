from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "Backend is working!"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/analyze-cv", methods=["POST", "OPTIONS"])
def analyze_cv():
    if request.method == "OPTIONS":
        return "", 204
    try:
        data = request.json or {}
        cv = data.get("cv", "")
        job = data.get("job", "")
        if not cv or not job:
            return jsonify({"error": "CV and job description are required"}), 400

        prompt = f"""
You are an expert ATS resume reviewer.

Analyze this CV against this job description.

Return:
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
        return jsonify({"result": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/cover-letter", methods=["POST", "OPTIONS"])
def cover_letter():
    if request.method == "OPTIONS":
        return "", 204
    try:
        data = request.json or {}
        name = data.get("name", "")
        role = data.get("role", "")
        company = data.get("company", "")
        skills = data.get("skills", "")

        if not name or not role or not company:
            return jsonify({"error": "Name, role, and company are required"}), 400

        prompt = f"""
You are an expert career writer.

Write a professional, short, persuasive cover letter.

Candidate Name: {name}
Target Role: {role}
Company: {company}
Key Skills: {skills}

Rules:
- Start with Dear Hiring Manager,
- 140 to 190 words
- Professional English
- Sound human, not generic AI
- Do not invent fake experience
- End with Sincerely, then candidate name
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return jsonify({"result": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/job-match", methods=["POST", "OPTIONS"])
def job_match():
    if request.method == "OPTIONS":
        return "", 204
    try:
        data = request.json or {}
        role = data.get("role", "")
        skills = data.get("skills", "")
        country = data.get("country", "")

        prompt = f"""
You are a career AI assistant.

Find job matches for:
Role: {role}
Skills: {skills}
Country: {country}

Return:
- 3 suitable job titles
- Why each job matches
- Missing skills
- Tips to improve chances
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return jsonify({"result": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/interview-prep", methods=["POST", "OPTIONS"])
def interview_prep():
    if request.method == "OPTIONS":
        return "", 204
    try:
        data = request.json or {}
        role = data.get("role", "")
        skills = data.get("skills", "")

        if not role:
            return jsonify({"error": "Role is required"}), 400

        prompt = f"""
You are an expert interview coach.

Prepare interview questions and answers for:
Role: {role}
Skills: {skills}

Return:
1) 5 technical questions + short strong answers
2) 5 behavioral questions + strong answers using STAR method
3) Tips to succeed in the interview
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return jsonify({"result": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/auto-fix-cv", methods=["POST", "OPTIONS"])
def auto_fix_cv():
    if request.method == "OPTIONS":
        return "", 204
    try:
        data = request.json or {}
        cv = data.get("cv", "")
        job = data.get("job", "")

        if not cv or not job:
            return jsonify({"error": "CV and job description are required"}), 400

        prompt = f"""
You are an expert resume writer and ATS specialist.

Rewrite the user's CV to better match the target job description.

Rules:
- Do not invent fake experience
- Keep the same education and real skills
- Improve wording professionally
- Add relevant keywords naturally
- Make it ATS-friendly
- Use clear sections
- Write in English

CV:
{cv}

Job Description:
{job}

Return:
1. Improved Professional Summary
2. Improved Skills Section
3. Improved Projects / Experience Bullet Points
4. Full Improved CV
5. Final Advice
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return jsonify({"result": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)