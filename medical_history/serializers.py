from rest_framework import serializers

from medical_history.models import Appointment, Patient, PatientAttachmentData, PatientTreatment, PatientDiagnostic, \
    TreatmentSession
from users.serializers import UserSerializer


class PatientAttachmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientAttachmentData
        fields = ("description", "link", "patient")


class PatientSerializer(serializers.ModelSerializer):
    attachments = PatientAttachmentDataSerializer(many=True)

    class Meta:
        model = Patient
        fields = "__all__"


class PatientTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientTreatment
        fields = "__all__"


class PatientDiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDiagnostic
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    patient = PatientSerializer()
    patient_diagnostic = PatientTreatmentSerializer()
    patient_treatment = PatientDiagnosticSerializer()

    class Meta:
        model = Appointment
        fields = "__all__"


class TreatmentSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    patient = PatientSerializer()
    patient_treatment = PatientDiagnosticSerializer()

    class Meta:
        model = TreatmentSession
        fields = "__all__"