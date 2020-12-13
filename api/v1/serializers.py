from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    img_link = serializers.URLField


class PatientSerializer(serializers.Serializer):
    name = serializers.CharField
    last_name = serializers.CharField
    phone_number = serializers.CharField


class MedicalHistorySummarySerializer(serializers.Serializer):
    summary = serializers.CharField
    patient = PatientSerializer
    images = ImageSerializer(many=True)
