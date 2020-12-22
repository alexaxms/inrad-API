from django.http import Http404
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from medical_history.models import Patient, Appointment
from medical_history.serializers import AppointmentSerializer, PatientSerializer


class AppointmentViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    serializer_class = AppointmentSerializer
    filterset_fields = ["user_id"]

    def get_queryset(self):
        try:
            patient = Patient.objects.get(id=self.kwargs['patient_pk'])
            return patient.appointment
        except Appointment.DoesNotExist:
            raise Http404


class PatientViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
