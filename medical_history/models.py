from django.db import models

from users.models import User


class Patient(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)


class Diagnostic(models.Model):
    name = models.CharField(max_length=255)
    pre_existing = models.BooleanField(default=False)


class Treatment(models.Model):
    name = models.CharField(max_length=255)


class Appointment(models.Model):
    summary = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="appointment", on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, related_name="appointment", on_delete=models.DO_NOTHING)


class MedicalAppointmentImage(models.Model):
    img_link = models.CharField(max_length=255)
    medical_appointment_summary = models.ForeignKey(Appointment, related_name="images",
                                                    on_delete=models.CASCADE)


class PatientTreatment(models.Model):
    start_date = models.DateField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment,  on_delete=models.CASCADE)


class PatientDiagnostic(models.Model):
    diagnostic_date = models.DateField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)