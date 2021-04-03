from rest_framework import serializers

from medical_history.models import (
    Appointment,
    Patient,
    PatientAttachmentData,
    PatientTreatment,
    DiseaseType,
    Treatment,
    TreatmentCategory,
    SymptomGroup,
    Symptom,
    TreatmentMachine,
    TreatmentMode,
    PatientDiagnostic,
    MedicalAppointmentImage,
    DiseaseCategory,
)
from users.serializers import UserSerializer


class DiseaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseCategory
        fields = "__all__"


class DiseaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseType
        fields = "__all__"


class PatientAttachmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientAttachmentData
        fields = ("description", "attachment", "name", "id")


class PatientDiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDiagnostic
        fields = (
            "diagnostic_date",
            "disease_type",
            "description",
            "disease_stage",
            "disease_aggressiveness",
            "id",
        )


class PatientTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientTreatment
        fields = (
            "start_date",
            "end_date",
            "treatment",
            "machine",
            "mode",
            "success",
            "id",
        )


class PatientDetailPatientDiagnosticSerializer(serializers.ModelSerializer):
    disease_type = DiseaseTypeSerializer()

    class Meta:
        model = PatientDiagnostic
        fields = "__all__"


class PatientDetailPatientTreatmentSerializer(serializers.ModelSerializer):
    treatment = serializers.CharField(source="treatment.name")
    machine = serializers.CharField(source="machine.name")
    mode = serializers.CharField(source="mode.name")

    class Meta:
        model = PatientTreatment
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    attachments = PatientAttachmentDataSerializer(many=True)
    diagnostics = PatientDetailPatientDiagnosticSerializer(many=True, read_only=True)
    treatments = PatientDetailPatientTreatmentSerializer(many=True, read_only=True)
    current_treatment = PatientDetailPatientTreatmentSerializer(read_only=True)
    current_diagnostic = PatientDetailPatientDiagnosticSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = "__all__"

    def create(self, validated_data):
        attachments_data = validated_data.pop("attachments")
        patient = Patient.objects.create(**validated_data)
        for attachment in attachments_data:
            PatientAttachmentData.objects.create(patient=patient, **attachment)
        return patient


class DetailAppointmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalAppointmentImage
        fields = "__all__"


class DetailAppointmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    patient_diagnostic = PatientTreatmentSerializer(read_only=True)
    patient_treatment = PatientDiagnosticSerializer(read_only=True)
    images = DetailAppointmentImageSerializer(many=True)

    class Meta:
        model = Appointment
        fields = "__all__"


class AppointmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalAppointmentImage
        fields = ("id", "name", "description", "image")


class AppointmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    patient_diagnostic = PatientTreatmentSerializer(read_only=True)
    patient_treatment = PatientDiagnosticSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"


class TreatmentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentCategory
        fields = "__all__"


class TreatmentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentMode
        fields = "__all__"


class TreatmentMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentMachine
        fields = "__all__"


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = "__all__"


class DetailTreatmentSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", required=False)

    class Meta:
        model = Treatment
        fields = ("id", "name", "category")


class DetailDiseaseTypeSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", required=False)

    class Meta:
        model = DiseaseType
        fields = ("id", "name", "code", "description", "category")


class SymptomGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomGroup
        fields = "__all__"


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = "__all__"


class DetailSymptomSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source="group.name", required=False)

    class Meta:
        model = Symptom
        fields = ("id", "name", "group")


class DetailPatientTreatmentSerializer(serializers.ModelSerializer):
    treatment = TreatmentSerializer()
    machine = serializers.CharField(source="machine.name")
    mode = serializers.CharField(source="mode.name")

    class Meta:
        model = PatientTreatment
        fields = "__all__"
