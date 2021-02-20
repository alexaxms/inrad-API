from django.http import Http404
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.viewsets import GenericViewSet

from medical_history.models import Patient, Appointment, DiseaseType, Treatment, TreatmentCategory, SymptomGroup, \
    Symptom
from medical_history.serializers import AppointmentSerializer, PatientSerializer, \
    DiseaseTypeSerializer, TreatmentSerializer, TreatmentCategorySerializer, \
    DetailTreatmentSerializer, SymptomGroupSerializer, SymptomSerializer, DetailSymptomSerializer


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
            return patient.appointments
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
    authentication_classes = [SessionAuthentication]


class DiseaseTypeViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    queryset = DiseaseType.objects.all()
    serializer_class = DiseaseTypeSerializer


class TreatmentViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    filterset_fields = ["name"]
    authentication_classes = [SessionAuthentication]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return DetailTreatmentSerializer
        return TreatmentSerializer


class TreatmentCategoryViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               GenericViewSet):
    queryset = TreatmentCategory.objects.all()
    serializer_class = TreatmentCategorySerializer
    filterset_fields = ["name"]
    authentication_classes = [SessionAuthentication]


class SymptomGroupViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          GenericViewSet):
    queryset = SymptomGroup.objects.all()
    serializer_class = SymptomGroupSerializer
    filterset_fields = ["name"]
    authentication_classes = [SessionAuthentication]


class SymptomViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Symptom.objects.all()
    filterset_fields = ["name"]
    authentication_classes = [SessionAuthentication]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return DetailSymptomSerializer
        return SymptomSerializer
