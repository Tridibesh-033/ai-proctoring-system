import requests
import os
import json
import re

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct"

def _safe_json_load(text: str):
    """
    Extract JSON safely from LLM response
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("Invalid JSON returned from LLM")

def generate_questions(job_desc: str, config: dict) -> list:
    prompt = f"""
You are an expert technical interviewer.

Generate interview questions STRICTLY in JSON format.

JOB DESCRIPTION:
{job_desc}

QUESTION RULES:

1. MCQ:
- Provide 4 options (A, B, C, D)
- Provide correct_answer (A/B/C/D)

2. Coding:
- Practical problem
- correct_answer = expected approach / logic summary

3. Audio:
- Spoken explanation question
- NO options
- NO correct_answer

4. Video:
- Confidence / system design / behavioral
- NO options
- NO correct_answer

CONFIG (STRICT):
{json.dumps(config, indent=2)}

OUTPUT FORMAT (JSON ARRAY ONLY):

[
  {{
    "question": "string",
    "type": "mcq | coding | audio | video",
    "difficulty": "easy | medium | hard",
    "options": {{"A": "", "B": "", "C": "", "D": ""}} | null,
    "correct_answer": "string" | null
  }}
]

IMPORTANT:
- Follow config counts exactly
- Do NOT add extra text
- Return ONLY JSON
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "AI Exam Generator"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 2000
        },
        timeout=60
    )

    content = response.json()["choices"][0]["message"]["content"]
    questions = _safe_json_load(content)

    cleaned = []

    for q in questions:
        qtype = q["type"]

        item = {
            "question": q["question"],
            "type": qtype,
            "difficulty": q["difficulty"],
            "options": None,
            "correct_answer": None
        }

        if qtype == "mcq":
            item["options"] = q.get("options")
            item["correct_answer"] = q.get("correct_answer")

        elif qtype == "coding":
            item["correct_answer"] = q.get("correct_answer")


        cleaned.append(item)

    return cleaned
