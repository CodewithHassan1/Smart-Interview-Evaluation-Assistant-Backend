from django.contrib import admin

from .models import CandidateEvaluation


@admin.register(CandidateEvaluation)
class CandidateEvaluationAdmin(admin.ModelAdmin):
    list_display = ("candidate_name", "position", "final_verdict", "created_at", "created_by")
    list_filter = ("position", "final_verdict", "created_at")
    search_fields = ("candidate_name", "raw_notes", "structured_report")
