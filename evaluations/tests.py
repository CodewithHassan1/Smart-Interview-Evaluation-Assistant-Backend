from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework.authtoken.models import Token

from .models import CandidateEvaluation


class CandidateEvaluationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="p@ssword123")
        self.token = Token.objects.create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    @patch("core.ai_client.AI_API_KEY", None)
    def test_create_evaluation_without_ai_key(self):
        response = self.client.post(
            "/api/evaluations/",
            {
                "candidate_name": "Test Candidate",
                "position": "Backend Intern",
                "raw_notes": "Solid Python skills, needs more REST experience.",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CandidateEvaluation.objects.count(), 1)
        evaluation = CandidateEvaluation.objects.first()
        self.assertIn("fallback report", evaluation.structured_report.lower())

    def test_list_evaluations(self):
        CandidateEvaluation.objects.create(
            candidate_name="Jane Doe",
            position="Frontend Developer",
            raw_notes="Good notes.",
            structured_report="Report.",
            final_verdict="Hire",
        )
        response = self.client.get("/api/evaluations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
