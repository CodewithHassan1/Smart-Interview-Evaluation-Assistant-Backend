import json
import os
import re

import requests

AI_API_URL = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions")
AI_API_KEY = os.getenv("GEMINI_API_KEY")
AI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = (
    "You are a high-accuracy interview evaluation assistant. "
    "Convert messy interviewer notes into a professional evaluation report. "
    "Extract candidate strengths, technical skills, and assessment categories. "
    "Return only valid JSON with the exact keys requested."
)

PROMPT_TEMPLATE = (
    "Candidate: {candidate_name}\n"
    "Position: {position}\n"
    "Raw interviewer notes:\n{raw_notes}\n\n"
    "Convert the above into a structured professional evaluation. "
    "Include a clear summary, a consistent scoring section, and a hiring recommendation. "
    "Output only valid JSON, with keys: structured_report, final_verdict, score_breakdown, skills_summary, reasoning. "
    "Provide scores between 1 and 10. "
    "If the notes include multiple strengths or challenges, extract them into the report narrative."
)


def extract_json(text):
    candidate = re.search(r"\{.*\}", text, re.S)
    if not candidate:
        return None
    try:
        return json.loads(candidate.group())
    except json.JSONDecodeError:
        cleaned = text[candidate.start():candidate.end()]
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return None


def transform_notes_to_report(raw_notes: str, candidate_name: str, position: str) -> dict:
    if not AI_API_KEY:
        return {
            "structured_report": (
                f"**Sample fallback report for {candidate_name}**\n" 
                "The assistant detected missing AI credentials and returned a professional placeholder."),
            "final_verdict": "No Hire",
            "score_breakdown": {
                "communication": 6,
                "technical": 6,
                "problem_solving": 6,
            },
            "skills_summary": {
                "technical_skills": ["Python", "API design", "Debugging"],
                "soft_skills": ["Clear communication", "Teamwork"],
            },
            "reasoning": "AI credentials were not configured, so this placeholder report is returned for development and demo purposes.",
        }

    payload = {
        "model": AI_MODEL,
        "temperature": 0.2,
        "max_tokens": 900,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": PROMPT_TEMPLATE.format(
                    candidate_name=candidate_name,
                    position=position,
                    raw_notes=raw_notes,
                ),
            },
        ],
    }

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(AI_API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    text = ""

    if "choices" in data and len(data["choices"]) > 0:
        text = data["choices"][0].get("message", {}).get("content", "")
    elif "output" in data and len(data["output"]) > 0:
        text = data["output"][0].get("content", [])[0].get("text", "")

    parsed = extract_json(text) or {}

    return {
        "structured_report": parsed.get("structured_report", text.strip()),
        "final_verdict": parsed.get("final_verdict", "No Hire"),
        "score_breakdown": parsed.get("score_breakdown", {}),
        "skills_summary": parsed.get("skills_summary", {}),
        "reasoning": parsed.get("reasoning", "AI output could not be parsed cleanly."),
    }
