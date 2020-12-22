from rest_framework import serializers

from medical_history.models import Appointment, Patient
from users.serializers import UserSerializer


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    patient = PatientSerializer()

    class Meta:
        model = Appointment
        fields = "__all__"
