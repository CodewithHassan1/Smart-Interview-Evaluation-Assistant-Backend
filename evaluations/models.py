from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class CandidateEvaluation(models.Model):
    VERDICT_CHOICES = [
        ("Strong Hire", "Strong Hire"),
        ("Hire", "Hire"),
        ("No Hire", "No Hire"),
    ]

    candidate_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    raw_notes = models.TextField()
    structured_report = models.TextField(blank=True)
    final_verdict = models.CharField(max_length=50, choices=VERDICT_CHOICES, default="No Hire")
    score_breakdown = models.JSONField(blank=True, null=True)
    skills_summary = models.JSONField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.candidate_name} — {self.position}"
