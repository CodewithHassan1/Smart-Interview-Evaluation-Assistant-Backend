import json
import logging
import os
import re

import requests

logger = logging.getLogger(__name__)

AI_API_URL = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions")
AI_API_KEY = os.getenv("GEMINI_API_KEY")
AI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = (
    "You are a high-accuracy interview evaluation assistant. "
    "Convert messy interviewer notes into a professional evaluation report. "
    "Extract candidate strengths, technical skills, and assessment categories. "
    "Return only valid JSON matching the exact schema requested."
)

PROMPT_TEMPLATE = (
    "Candidate: {candidate_name}\n"
    "Position: {position}\n"
    "Raw interviewer notes:\n{raw_notes}\n\n"
    "Convert the above notes into a structured professional evaluation JSON object. "
    "The output JSON MUST follow this exact schema structure:\n"
    "{{\n"
    '  "structured_report": "A detailed, professional narrative summary of the candidate\'s performance, strengths, and areas for improvement.",\n'
    '  "final_verdict": "Must be exactly one of: \'Strong Hire\', \'Hire\', or \'No Hire\'.",\n'
    '  "score_breakdown": {{\n'
    '    "communication": <integer score between 1 and 10>,\n'
    '    "technical": <integer score between 1 and 10>,\n'
    '    "problem_solving": <integer score between 1 and 10>\n'
    '  }},\n'
    '  "skills_summary": {{\n'
    '    "technical_skills": [<array of extracted technical skill strings like libraries, frameworks, languages>],\n'
    '    "soft_skills": [<array of extracted soft skill strings like collaboration, communication, leadership>]\n'
    '  }},\n'
    '  "reasoning": "A short explanation justifying the score breakdown and final recommendation."\n'
    "}}\n"
    "Do not include any wrapping markdown like ```json ... ```. Output raw JSON only."
)


def extract_json(text):
    """Extract JSON from AI response, handling markdown fences and thinking output."""
    # Strip markdown code fences (```json ... ``` or ``` ... ```)
    stripped = re.sub(r"```(?:json)?\s*", "", text)
    stripped = re.sub(r"```", "", stripped).strip()

    candidate = re.search(r"\{.*\}", stripped, re.S)
    if not candidate:
        return None
    try:
        return json.loads(candidate.group())
    except json.JSONDecodeError:
        # Try cleaning control characters
        cleaned = re.sub(r"[\x00-\x1f]+", " ", candidate.group())
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON from AI response: %s", candidate.group()[:200])
            return None


def normalize_ai_payload(parsed: dict, candidate_name: str) -> dict:
    """
    Normalizes the JSON response from the LLM to fit the exact database schema
    and front-end expectations (preventing broken scorecards or skills formats).
    """
    # 1. Normalize structured_report
    report = parsed.get("structured_report", "").strip()
    if not report:
        report = f"Evaluation report for {candidate_name}."

    # 2. Normalize final_verdict
    verdict = parsed.get("final_verdict", "No Hire")
    if not isinstance(verdict, str):
        verdict = "No Hire"
    
    verdict_clean = verdict.strip().lower()
    if "strong" in verdict_clean:
        final_verdict = "Strong Hire"
    elif "no" in verdict_clean:
        final_verdict = "No Hire"
    else:
        final_verdict = "Hire"

    # 3. Normalize score_breakdown
    raw_scores = parsed.get("score_breakdown", {})
    if not isinstance(raw_scores, dict):
        raw_scores = {}
    
    def find_score(keys, default=5):
        for k, v in raw_scores.items():
            if any(word in k.lower() for word in keys):
                try:
                    return int(float(v))
                except (ValueError, TypeError):
                    continue
        return default

    score_breakdown = {
        "communication": find_score(["communication", "comm", "soft"], 5),
        "technical": find_score(["technical", "tech", "coding", "skill"], 5),
        "problem_solving": find_score(["problem", "solving", "critical", "thinking", "reasoning"], 5),
    }

    # 4. Normalize skills_summary
    raw_skills = parsed.get("skills_summary", {})
    technical_skills = []
    soft_skills = []

    if isinstance(raw_skills, list):
        # LLM returned a flat list. Split into technical and soft based on keywords
        tech_keywords = ["react", "tailwind", "python", "javascript", "js", "api", "database", "sql", "git", "css", "html", "django", "postgres"]
        for s in raw_skills:
            if not isinstance(s, str):
                continue
            if any(keyword in s.lower() for keyword in tech_keywords):
                technical_skills.append(s)
            else:
                soft_skills.append(s)
    elif isinstance(raw_skills, dict):
        # Extract technical skills
        t_skills = raw_skills.get("technical_skills", [])
        if isinstance(t_skills, list):
            technical_skills = [str(x) for x in t_skills]
        else:
            for k, v in raw_skills.items():
                if "tech" in k.lower() and isinstance(v, list):
                    technical_skills = [str(x) for x in v]

        # Extract soft skills
        s_skills = raw_skills.get("soft_skills", [])
        if isinstance(s_skills, list):
            soft_skills = [str(x) for x in s_skills]
        else:
            for k, v in raw_skills.items():
                if ("soft" in k.lower() or "inter" in k.lower()) and isinstance(v, list):
                    soft_skills = [str(x) for x in v]

    skills_summary = {
        "technical_skills": technical_skills,
        "soft_skills": soft_skills
    }

    return {
        "structured_report": report,
        "final_verdict": final_verdict,
        "score_breakdown": score_breakdown,
        "skills_summary": skills_summary,
        "reasoning": parsed.get("reasoning", "Successfully parsed report.")
    }


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
        "max_tokens": 2048,
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

    response = requests.post(AI_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    text = ""

    if "choices" in data and len(data["choices"]) > 0:
        text = data["choices"][0].get("message", {}).get("content", "")
    elif "output" in data and len(data["output"]) > 0:
        text = data["output"][0].get("content", [])[0].get("text", "")

    logger.info("AI raw response (first 500 chars): %s", text[:500])
    parsed = extract_json(text) or {}
    return normalize_ai_payload(parsed, candidate_name)
