from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CandidateEvaluationViewSet, LoginView, SignupView

router = DefaultRouter()
router.register(r"evaluations", CandidateEvaluationViewSet, basename="evaluation")

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("", include(router.urls)),
]
