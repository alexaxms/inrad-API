import json
import os

import pika
from django.db import models

from users.models import User


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
    age = models.IntegerField()
    blood_type = models.CharField(max_length=4)

    def __str__(self):
        return self.name

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "gender": self.gender,
            "identifier": self.identifier,
            "age": self.age,
            "blood_type": self.blood_type,
            "attachments": [attachment.to_dict() for attachment in self.attachments.all()]
        }


class PatientAttachmentData(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    patient = models.ForeignKey(Patient, related_name="attachments", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "img_link": self.link
        }


class Diagnostic(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class SymptomGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Symptom(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(SymptomGroup, related_name="symptoms", on_delete=models.CASCADE)
    diagnostic = models.ForeignKey(Diagnostic, related_name="symptoms", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Treatment(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DiseaseType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DiseaseStage(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Disease(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(DiseaseType, related_name="diseases", on_delete=models.CASCADE)
    stage = models.ForeignKey(DiseaseStage, related_name="diseases", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.type.name,
            "stage": self.stage.name
        }


class PatientTreatment(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, default=None)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    success = models.BooleanField(null=True, default=None)

    def __str__(self):
        return f'{self.patient.name} {self.treatment.name}'

    def to_dict(self) -> dict:
        return {
            "start_date": str(self.start_date),
            "end_date": str(self.end_date) if self.end_date else None,
            "treatment_name": self.treatment.name,
            "success": self.success
        }


class TreatmentSession(models.Model):
    summary = models.TextField()
    user = models.ForeignKey(User, related_name="treatment_sessions", on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, related_name="treatment_sessions", on_delete=models.DO_NOTHING)
    patient_treatment = models.ForeignKey(PatientTreatment, related_name="treatment_sessions",
                                          on_delete=models.DO_NOTHING)
    disease = models.ForeignKey(Disease, related_name="treatment_sessions", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.patient.name} - {str(self.created_at)}'

    def save(self, *args, **kwargs):
        super(TreatmentSession, self).save(*args, **kwargs)
        self.send_treatment_session_to_rmq()

    def send_treatment_session_to_rmq(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv("RABBIT_HOST")))
        channel = connection.channel()
        channel.queue_declare(queue='inrad')
        channel.basic_publish(exchange='',
                              routing_key='inrad',
                              body=json.dumps(self.to_dict()))
        print(" [x] Sent to RabbitMQ")
        connection.close()

    def to_dict(self) -> dict:
        return {
            "type": "SESSION",
            "summary": self.summary,
            "user": self.user.to_dict(),
            "patient": self.patient.to_dict(),
            "patient_treatment": self.patient_treatment.to_dict(),
            "disease": self.disease.to_dict(),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }


class TreatmentSessionImage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    img_link = models.URLField()
    treatment_session = models.ForeignKey(TreatmentSession, related_name="images",
                                          on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "img_link": self.img_link
        }


class PatientDiagnostic(models.Model):
    diagnostic_date = models.DateField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.patient.name} {self.diagnostic.name}'

    def to_dict(self) -> dict:
        return {
            "diagnostic_date": str(self.diagnostic_date),
            "name": self.diagnostic.name,
            "description": self.diagnostic.description
        }


class Appointment(models.Model):
    summary = models.TextField()
    user = models.ForeignKey(User, related_name="appointments", on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, related_name="appointments", on_delete=models.DO_NOTHING)
    patient_diagnostic = models.ForeignKey(PatientDiagnostic, on_delete=models.DO_NOTHING)
    patient_treatment = models.ForeignKey(PatientTreatment, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Appointment, self).save(*args, **kwargs)
        self.send_treatment_session_to_rmq()

    def __str__(self):
        return f'{self.patient.name} - {str(self.created_at)}'

    def send_treatment_session_to_rmq(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv("RABBIT_HOST")))
        channel = connection.channel()
        channel.queue_declare(queue='inrad')
        channel.basic_publish(exchange='',
                              routing_key='inrad',
                              body=json.dumps(self.to_dict()))
        print(" [x] Sent to RabbitMQ")
        connection.close()

    def to_dict(self) -> dict:
        return {
            "type": "APPOINTMENT",
            "summary": self.summary,
            "user": self.user.to_dict(),
            "patient": self.patient.to_dict(),
            "patient_treatment": self.patient_treatment.to_dict() if self.patient_treatment else None,
            "diagnostic": self.patient_diagnostic.to_dict(),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }


class MedicalAppointmentImage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    img_link = models.URLField()
    medical_appointment_summary = models.ForeignKey(Appointment, related_name="images",
                                                    on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "img_link": self.img_link
        }
