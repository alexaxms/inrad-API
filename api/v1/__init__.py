from rest_framework import viewsets
from rest_framework.response import Response

from api.v1.serializers import MedicalHistorySummarySerializer
from medical_history.medical_history_facade import list_medical_appointment_summaries


class MedicalHistorySummaryViewSet(viewsets.GenericViewSet):
    permission_classes = ()

    def list(self, request):
        summaries = list_medical_appointment_summaries()
        serializer = MedicalHistorySummarySerializer(summaries, many=True)
        return Response(serializer.data)
