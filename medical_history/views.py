from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from medical_history.models import (
    Patient,
    Appointment,
    DiseaseType,
    Treatment,
    TreatmentCategory,
    SymptomGroup,
    Symptom,
    TreatmentMachine,
    TreatmentMode,
    PatientDiagnostic,
    PatientTreatment,
    PatientAttachmentData,
    DiseaseCategory,
    MedicalAppointmentImage,
)
from medical_history.serializers import (
    AppointmentSerializer,
    PatientSerializer,
    DiseaseTypeSerializer,
    TreatmentSerializer,
    TreatmentCategorySerializer,
    SymptomGroupSerializer,
    SymptomSerializer,
    DetailSymptomSerializer,
    TreatmentMachineSerializer,
    TreatmentModeSerializer,
    PatientDiagnosticSerializer,
    PatientTreatmentSerializer,
    DetailPatientTreatmentSerializer,
    PatientAttachmentDataSerializer,
    PatientDetailPatientDiagnosticSerializer,
    DiseaseCategorySerializer,
    DetailDiseaseTypeSerializer,
    DetailTreatmentSerializer,
    DetailAppointmentSerializer,
    AppointmentImageSerializer,
)


class AppointmentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = AppointmentSerializer
    filterset_fields = ["user_id"]

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return DetailAppointmentSerializer
        return AppointmentSerializer

    def get_queryset(self):
        try:
            patient = Patient.objects.get(id=self.kwargs["patient_pk"])
            return patient.appointments
        except Appointment.DoesNotExist:
            raise Http404

    def perform_create(self, serializer):
        patient = Patient.objects.get(id=self.kwargs["patient_pk"])
        treatment = patient.treatments.last()
        diagnostic = patient.diagnostics.last()
        serializer.save(
            patient_id=self.kwargs["patient_pk"],
            user_id=serializer.context["request"].user.id,
            patient_diagnostic=diagnostic,
            patient_treatment=treatment,
        )


class PatientViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated,)


class DiseaseTypeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = DiseaseType.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return DetailDiseaseTypeSerializer
        return DiseaseTypeSerializer

    @method_decorator(cache_page(60 * 60 * 24))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class DiseaseCategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = DiseaseCategory.objects.all()
    serializer_class = DiseaseCategorySerializer
    filterset_fields = ["name"]
    permission_classes = (IsAuthenticated,)

    @method_decorator(cache_page(60 * 60 * 24))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class TreatmentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    filterset_fields = ["name"]
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return DetailTreatmentSerializer
        return TreatmentSerializer


class TreatmentCategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = TreatmentCategory.objects.all()
    serializer_class = TreatmentCategorySerializer
    filterset_fields = ["name"]
    permission_classes = (IsAuthenticated,)


class TreatmentMachineViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = TreatmentMachine.objects.all()
    serializer_class = TreatmentMachineSerializer
    filterset_fields = ["name"]
    permission_classes = (IsAuthenticated,)


class TreatmentModeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = TreatmentMode.objects.all()
    serializer_class = TreatmentModeSerializer
    filterset_fields = ["name"]
    permission_classes = (IsAuthenticated,)


class SymptomGroupViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = SymptomGroup.objects.all()
    serializer_class = SymptomGroupSerializer
    filterset_fields = ["name"]
    permission_classes = (IsAuthenticated,)


class SymptomViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Symptom.objects.all()
    filterset_fields = ["name"]
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return DetailSymptomSerializer
        return SymptomSerializer


class SymptomByGroupViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = DetailSymptomSerializer
    filterset_fields = ["name"]
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        symptoms = Symptom.objects.filter(group_id=self.kwargs["symptom_group_pk"])
        return symptoms.all()


class PatientDiagnosticViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return PatientDetailPatientDiagnosticSerializer
        return PatientDiagnosticSerializer

    def get_queryset(self):
        attachments = PatientDiagnostic.objects.filter(
            patient_id=self.kwargs["patient_pk"]
        )
        return attachments.all()

    def perform_create(self, serializer):
        serializer.save(patient_id=self.kwargs["patient_pk"])


class PatientTreatmentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        patient_diagnostics = PatientTreatment.objects.filter(
            patient_id=self.kwargs["patient_pk"]
        )
        return patient_diagnostics.all()

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return DetailPatientTreatmentSerializer
        return PatientTreatmentSerializer

    def perform_create(self, serializer):
        serializer.save(patient_id=self.kwargs["patient_pk"])


class PatientAttachmentDataViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = PatientAttachmentDataSerializer

    def get_queryset(self):
        attachments = PatientAttachmentData.objects.filter(
            patient_id=self.kwargs["patient_pk"]
        )
        return attachments.all()

    def perform_create(self, serializer):
        serializer.save(patient_id=self.kwargs["patient_pk"])


class PatientAppointmentImageViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentImageSerializer

    def get_queryset(self):
        images = MedicalAppointmentImage.objects.filter(
            appointment_id=self.kwargs["appointment_pk"],
            appointment__patient=self.kwargs["patient_pk"],
        )
        return images.all()

    def perform_create(self, serializer):
        serializer.save(appointment_id=self.kwargs["appointment_pk"])
