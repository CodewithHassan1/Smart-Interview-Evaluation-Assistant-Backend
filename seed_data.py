import os
from pathlib import Path

import django
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from evaluations.models import CandidateEvaluation

samples = [
    {
        "candidate_name": "Amina Khan",
        "position": "Frontend Developer",
        "raw_notes": "Good HTML/CSS, some React hooks knowledge, struggled with async logic, communicates clearly, positive attitude.",
        "structured_report": "Amina demonstrates strong frontend foundations in HTML and CSS with a solid understanding of React hooks. She presented clear communication and eagerness to improve, though she needs more practice with async data handling. Her teamwork attitude is positive and she would be a good fit for a supportive frontend intern role.",
        "final_verdict": "Hire",
        "score_breakdown": {"communication": 8, "technical": 7, "problem_solving": 6},
        "skills_summary": {"technical_skills": ["HTML", "CSS", "React", "JavaScript"], "soft_skills": ["Communication", "Teamwork"]},
    },
    {
        "candidate_name": "Bilal Ahmed",
        "position": "Backend Intern",
        "raw_notes": "Understands Django models, asks about database normalization, slow on REST endpoints design but good debugging flow, neat code style, needs help with deployment concepts.",
        "structured_report": "Bilal has a good grasp of backend fundamentals and Django models. His debugging process is structured, and he understands database normalization. He needs mentorship on REST endpoint design and deployment patterns, but he shows strong potential for a backend intern role.",
        "final_verdict": "Strong Hire",
        "score_breakdown": {"communication": 7, "technical": 8, "problem_solving": 8},
        "skills_summary": {"technical_skills": ["Django", "PostgreSQL", "REST APIs"], "soft_skills": ["Problem Solving", "Attention to Detail"]},
    },
    {
        "candidate_name": "Neha Patel",
        "position": "Full Stack Developer",
        "raw_notes": "Strong logic, fast with node and express, some uncertainty on state management in React, excellent presentation, good mentoring potential.",
        "structured_report": "Neha delivers strong full stack abilities with clear backend knowledge in Node and Express. Her presentation skills are excellent and she has leadership potential. She should sharpen React state management before taking on an advanced full stack role.",
        "final_verdict": "Hire",
        "score_breakdown": {"communication": 9, "technical": 7, "problem_solving": 8},
        "skills_summary": {"technical_skills": ["Node.js", "Express", "React", "SQL"], "soft_skills": ["Presentation", "Leadership"]},
    },
    {
        "candidate_name": "Sameer Rao",
        "position": "QA Engineer",
        "raw_notes": "Focuses on test cases, good automation instincts, not deep in Selenium yet, asks about CI/CD, clear documentation habits.",
        "structured_report": "Sameer shows a strong QA mindset with attention to test coverage and documentation. He is building automation skills and already asks the right questions about CI/CD. With coaching on Selenium and test frameworks, he would be a dependable QA engineer intern.",
        "final_verdict": "Hire",
        "score_breakdown": {"communication": 8, "technical": 6, "problem_solving": 7},
        "skills_summary": {"technical_skills": ["Test Planning", "Automation", "CI/CD"], "soft_skills": ["Documentation", "Collaboration"]},
    },
    {
        "candidate_name": "Sara Malik",
        "position": "Product Designer",
        "raw_notes": "Strong UX thinking, uses Figma, good user empathy, unclear on design system versioning, needs deeper prototyping experience.",
        "structured_report": "Sara brings strong UX instincts and user empathy, with clear skill in Figma and early-stage design. She should deepen her prototyping workflow and design system governance, but she already fits well within a collaborative design team.",
        "final_verdict": "Hire",
        "score_breakdown": {"communication": 9, "technical": 6, "problem_solving": 7},
        "skills_summary": {"technical_skills": ["Figma", "UX Research", "Wireframing"], "soft_skills": ["Empathy", "Collaboration"]},
    },
]

CandidateEvaluation.objects.all().delete()
for sample in samples:
    CandidateEvaluation.objects.create(
        candidate_name=sample["candidate_name"],
        position=sample["position"],
        raw_notes=sample["raw_notes"],
        structured_report=sample["structured_report"],
        final_verdict=sample["final_verdict"],
        score_breakdown=sample["score_breakdown"],
        skills_summary=sample["skills_summary"],
    )

print("Seed data loaded successfully.")
