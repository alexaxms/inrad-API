from rest_framework import serializers

from medical_history.models import Appointment, Patient, PatientAttachmentData, PatientTreatment, TreatmentSession, \
    Disease, DiseaseType, DiseaseStage, Treatment, TreatmentCategory
from users.serializers import UserSerializer


class DiseaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseType
        fields = "__all__"


class DiseaseStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseStage
        fields = "__all__"


class DiseaseSerializer(serializers.ModelSerializer):
    type = DiseaseTypeSerializer(read_only=True)
    stage = DiseaseStageSerializer(read_only=True)

    class Meta:
        model = Disease
        fields = "__all__"


class PatientAttachmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientAttachmentData
        fields = ("description", "link", "patient")


class PatientSerializer(serializers.ModelSerializer):
    attachments = PatientAttachmentDataSerializer(many=True)

    class Meta:
        model = Patient
        fields = "__all__"

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments')
        patient = Patient.objects.create(**validated_data)
        for attachment in attachments_data:
            PatientAttachmentData.objects.create(patient=patient, **attachment)
        return patient


class PatientTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientTreatment
        fields = "__all__"


class PatientDiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientTreatment
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
    disease = DiseaseSerializer()

    class Meta:
        model = TreatmentSession
        fields = "__all__"


class TreatmentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentCategory
        fields = "__all__"


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = "__all__"
