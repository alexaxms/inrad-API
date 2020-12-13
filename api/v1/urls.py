from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from api.v1 import MedicalHistorySummaryViewSet

router = routers.SimpleRouter()
router.register("medical_history_summaries", MedicalHistorySummaryViewSet, basename="medical-history-summaries")

urlpatterns = []

urlpatterns.append(url(r"v1/", include(router.urls)))
