import json

import pika
from django.db import models

from users.models import User


class Patient(models.Model):
    GENDER = (
        ("Masculino", "Masculino"),
        ("Femenino", "Femenino"),
    )
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=GENDER)
    age = models.IntegerField()
    blood_type = models.CharField(max_length=4)

    def __str__(self):
        return self.name


class PatientAttachmentData(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    patient = models.ForeignKey(Patient, related_name="attachments", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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


class TreatmentSession(models.Model):
    summary = models.TextField()
    user = models.ForeignKey(User, related_name="treatment_sessions", on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, related_name="treatment_sessions", on_delete=models.DO_NOTHING)
    patient_treatment = models.ForeignKey(Treatment, related_name="treatment_sessions", on_delete=models.DO_NOTHING)
    disease = models.ForeignKey(Disease, related_name="treatment_sessions", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.patient.name} - {str(self.created_at)}'

    def save(self, *args, **kwargs):
        super(TreatmentSession, self).save(*args, **kwargs)
        self.send_treatment_session_to_rmq()

    def send_treatment_session_to_rmq(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='inrad')
        channel.basic_publish(exchange='',
                              routing_key='inrad',
                              body=json.dumps(self.send_treatment_session_body()))
        print(" [x] Sent to RabbitMQ")
        connection.close()

    def send_treatment_session_body(self) -> dict:
        return {
            "summary": self.summary,
            "user": self.user.first_name,
            "patient": {},
            "disease": self.disease.name,
            "created_at": str(self.created_at)
        }


class TreatmentSessionImage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    img_link = models.URLField()
    treatment_session = models.ForeignKey(TreatmentSession, related_name="images",
                                          on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PatientTreatment(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, default=None)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    success = models.BooleanField(null=True, default=None)

    def __str__(self):
        return f'{self.patient.name} {self.treatment.name}'


class PatientDiagnostic(models.Model):
    diagnostic_date = models.DateField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.patient.name} {self.diagnostic.name}'


class Appointment(models.Model):
    summary = models.TextField()
    user = models.ForeignKey(User, related_name="appointments", on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, related_name="appointments", on_delete=models.DO_NOTHING)
    patient_diagnostic = models.ForeignKey(PatientDiagnostic, on_delete=models.DO_NOTHING)
    patient_treatment = models.ForeignKey(PatientTreatment, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.patient.name} - {str(self.created_at)}'


class MedicalAppointmentImage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    img_link = models.URLField()
    medical_appointment_summary = models.ForeignKey(Appointment, related_name="images",
                                                    on_delete=models.CASCADE)

    def __str__(self):
        return self.name
