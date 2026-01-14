import requests
import os
import re


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not found in environment")

MODEL = "mistralai/mistral-7b-instruct" 

def openrouter_resume_score(resume_text: str, job_text: str) -> float:
    url = "https://openrouter.ai/api/v1/chat/completions"

    prompt = f"""
You are an ATS resume scoring engine.

Task:
Evaluate how well the resume matches the job description.

Scoring Rules:
- Score must be between 0 and 100
- Focus on REQUIRED skills, tools, and technologies
- Consider internships, projects, and hands-on experience
- Also consider achievements, research & publications and relavent skill Certification
- Do NOT reward irrelevant content
- Be strict but realistic (no perfect scores)
- Missing skills must reduce the score

Output Rules:
- Return ONLY a single number
- No text, no explanation, no JSON
- Example output: 72.5

Job Description:
{job_text}

Resume:
{resume_text}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Resume Scorer"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1, 
        "max_tokens": 20
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"].strip()

    match = re.search(r"\d+(\.\d+)?", content)
    if not match:
        raise ValueError(f"Invalid score returned by LLM: {content}")

    score = float(match.group())

    return round(min(score, 92.0), 2)
