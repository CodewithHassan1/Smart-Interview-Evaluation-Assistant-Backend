import logging

from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response

from core.ai_client import transform_notes_to_report
from .models import CandidateEvaluation
from .serializers import (
    CandidateEvaluationSerializer,
    LoginSerializer,
    SignupSerializer,
    UserSerializer,
)

logger = logging.getLogger(__name__)


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data})


class CandidateEvaluationViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateEvaluationSerializer
    queryset = CandidateEvaluation.objects.select_related("created_by").all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        raw_notes = serializer.validated_data.get("raw_notes")
        candidate_name = serializer.validated_data.get("candidate_name")
        position = serializer.validated_data.get("position")

        try:
            ai_payload = transform_notes_to_report(
                raw_notes=raw_notes,
                candidate_name=candidate_name,
                position=position,
            )
        except Exception as exc:
            ai_payload = {
                "structured_report": (
                    "The AI report generation failed due to a backend service error. "
                    "Please verify the Gemini API credentials and retry."
                ),
                "final_verdict": "No Hire",
                "score_breakdown": {"communication": 0, "technical": 0, "problem_solving": 0},
                "skills_summary": {"technical_skills": [], "soft_skills": []},
            }
            logger.exception("AI evaluation failure: %s", exc)

        serializer.save(
            created_by=self.request.user,
            structured_report=ai_payload.get("structured_report", ""),
            final_verdict=ai_payload.get("final_verdict", "No Hire"),
            score_breakdown=ai_payload.get("score_breakdown", {}),
            skills_summary=ai_payload.get("skills_summary", {}),
        )

    @action(detail=False, methods=["get"], url_path="current-user")
    def current_user(self, request):
        return Response(UserSerializer(request.user).data)
