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


class PatientAttachmentData(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    link = models.URLField()
    patient = models.ForeignKey(Patient, related_name="attachments", on_delete=models.CASCADE)


class Diagnostic(models.Model):
    name = models.CharField(max_length=255)


class SymptomGroup(models.Model):
    name = models.CharField(max_length=255)


class Symptom(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(SymptomGroup, related_name="symptoms", on_delete=models.CASCADE)
    diagnostic = models.ForeignKey(Diagnostic, related_name="symptoms", on_delete=models.CASCADE)


class Treatment(models.Model):
    name = models.CharField(max_length=255)


class DiseaseType(models.Model):
    name = models.CharField(max_length=255)


class DiseaseStage(models.Model):
    name = models.CharField(max_length=255)


class Disease(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(DiseaseType, related_name="diseases", on_delete=models.CASCADE)
    stage = models.ForeignKey(DiseaseStage, related_name="diseases", on_delete=models.CASCADE)


class TreatmentSession(models.Model):
    summary = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="treatment_sessions", on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, related_name="treatment_sessions", on_delete=models.DO_NOTHING)
    patient_treatment = models.ForeignKey(Treatment, related_name="treatment_sessions", on_delete=models.DO_NOTHING)
    disease = models.ForeignKey(Disease, related_name="treatment_sessions", on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        super(TreatmentSession, self).save(*args, **kwargs)
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='sessions')
        for i in range(100):
            channel.basic_publish(exchange='',
                                  routing_key='hello',
                                  body=self.summary)
        print(" [x] Sent 'Hello World!'")
        connection.close()


class TreatmentSessionImage(models.Model):
    img_link = models.URLField()
    treatment_session = models.ForeignKey(TreatmentSession, related_name="images",
                                          on_delete=models.CASCADE)


class PatientTreatment(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, default=None)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    success = models.BooleanField(null=True, default=None)


class PatientDiagnostic(models.Model):
    diagnostic_date = models.DateField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)


class Appointment(models.Model):
    summary = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="appointments", on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, related_name="appointments", on_delete=models.DO_NOTHING)
    patient_diagnostic = models.ForeignKey(PatientDiagnostic, on_delete=models.DO_NOTHING)
    patient_treatment = models.ForeignKey(PatientTreatment, on_delete=models.DO_NOTHING, null=True)


class MedicalAppointmentImage(models.Model):
    img_link = models.URLField()
    medical_appointment_summary = models.ForeignKey(Appointment, related_name="images",
                                                    on_delete=models.CASCADE)
