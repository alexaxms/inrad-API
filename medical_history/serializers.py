from rest_framework import serializers

from medical_history.models import Appointment, Patient, PatientAttachmentData, PatientTreatment, \
    DiseaseType, Treatment, TreatmentCategory, SymptomGroup, Symptom
from users.serializers import UserSerializer


class DiseaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseType
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


class TreatmentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentCategory
        fields = "__all__"


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = "__all__"


class DetailTreatmentSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', required=False)

    class Meta:
        model = Treatment
        fields = ("id", "name", "category")


class SymptomGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomGroup
        fields = "__all__"


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = "__all__"


class DetailSymptomSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name', required=False)

    class Meta:
        model = Symptom
        fields = ("id", "name", "group")
