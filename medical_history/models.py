import json
import os

import pika
from django.db import models

from users.models import User


class MedicalForecast(models.Model):
    name = models.CharField(max_length=100)


class HealthFacility(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)


class Patient(models.Model):
    GENDER = (
        ("Masculino", "Masculino"),
        ("Femenino", "Femenino"),
    )
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=13)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=GENDER)
    birth_date = models.DateField()
    health_facility = models.ForeignKey(
        HealthFacility,
        related_name="derived_patients",
        null=True,
        on_delete=models.DO_NOTHING,
    )
    medical_forecast = models.ForeignKey(
        MedicalForecast,
        related_name="related_patients",
        null=True,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return self.name

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "gender": self.gender,
            "identifier": self.identifier,
            "birth_date": self.birth_date,
            "attachments": [
                attachment.to_dict() for attachment in self.attachments.all()
            ],
        }

    @property
    def current_treatment(self):
        return self.treatments.last()

    @property
    def current_diagnostic(self):
        return self.diagnostics.last()


class PatientAttachmentData(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    attachment = models.FileField()
    patient = models.ForeignKey(
        Patient, related_name="attachments", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "img_link": self.link,
        }


class SymptomGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Symptom(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(
        SymptomGroup, related_name="symptoms", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class TreatmentCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TreatmentMode(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TreatmentMachine(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Treatment(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        TreatmentCategory, related_name="treatments", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class DiseaseCategory(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DiseaseType(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        DiseaseCategory, related_name="diseases", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class PatientTreatment(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, default=None)
    patient = models.ForeignKey(
        Patient, related_name="treatments", on_delete=models.CASCADE
    )
    treatment = models.ForeignKey(
        Treatment, related_name="treatments", on_delete=models.CASCADE
    )
    machine = models.ForeignKey(
        TreatmentMachine, related_name="treatments", on_delete=models.CASCADE
    )
    mode = models.ForeignKey(
        TreatmentMode, related_name="treatments", on_delete=models.CASCADE
    )
    success = models.BooleanField(null=True, default=None)

    def __str__(self):
        return f"{self.patient.name} {self.treatment.name}"

    def to_dict(self) -> dict:
        return {
            "start_date": str(self.start_date),
            "end_date": str(self.end_date) if self.end_date else None,
            "treatment_name": self.treatment.name,
            "success": self.success,
        }


class PatientDiagnostic(models.Model):
    diagnostic_date = models.DateField()
    patient = models.ForeignKey(
        Patient, related_name="diagnostics", on_delete=models.CASCADE
    )
    disease_type = models.ForeignKey(
        DiseaseType, related_name="diagnostics", on_delete=models.CASCADE
    )
    description = models.TextField()
    disease_stage = models.IntegerField()
    disease_aggressiveness = models.IntegerField()

    def __str__(self):
        return f"{self.patient.name} {self.diagnostic_date}"


class Appointment(models.Model):
    summary = models.TextField()
    date = models.DateField()
    user = models.ForeignKey(
        User, related_name="appointments", on_delete=models.DO_NOTHING
    )
    patient = models.ForeignKey(
        Patient, related_name="appointments", on_delete=models.DO_NOTHING
    )
    patient_diagnostic = models.ForeignKey(
        PatientDiagnostic, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    patient_treatment = models.ForeignKey(
        PatientTreatment, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Appointment, self).save(*args, **kwargs)
        # self.send_treatment_session_to_rmq()

    def __str__(self):
        return f"{self.patient.name} - {str(self.created_at)}"

    def send_treatment_session_to_rmq(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(os.getenv("RABBIT_HOST"))
        )
        channel = connection.channel()
        channel.queue_declare(queue="inrad")
        channel.basic_publish(
            exchange="", routing_key="inrad", body=json.dumps(self.to_dict())
        )
        print(" [x] Sent to RabbitMQ")
        connection.close()

    def to_dict(self) -> dict:
        return {
            "type": "APPOINTMENT",
            "summary": self.summary,
            "user": self.user.to_dict(),
            "patient": self.patient.to_dict(),
            "patient_treatment": self.patient_treatment.to_dict()
            if self.patient_treatment
            else None,
            "diagnostic": self.patient_diagnostic.to_dict(),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


class MedicalAppointmentImage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.FileField()
    appointment = models.ForeignKey(
        Appointment, related_name="images", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class MedicalAppointmentSymptom(models.Model):
    symptom = models.ForeignKey(
        Symptom, related_name="appointments", on_delete=models.DO_NOTHING
    )
    appointment = models.ForeignKey(
        Appointment, related_name="symptoms", on_delete=models.DO_NOTHING
    )
