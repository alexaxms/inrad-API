from django.db import models

from users.models import User


class Patient(models.Model):
    name = models.CharField
    last_name = models.CharField
    phone_number = models.CharField


class Diagnostic(models.Model):
    name = models.CharField
    pre_existing = models.BooleanField


class Treatment(models.Model):
    name = models.CharField


class MedicalAppointmentSummary(models.Model):
    summary = models.CharField
    user = models.ForeignKey(User, related_name="medical_appointment_summaries", on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, related_name="medical_appointment_summaries", on_delete=models.DO_NOTHING)


class MedicalAppointmentImage(models.Model):
    img_link = models.CharField
    medical_appointment_summary = models.ForeignKey(MedicalAppointmentSummary, related_name="images",
                                                    on_delete=models.CASCADE)


class PatientTreatment(models.Model):
    start_date = models.DateField
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment,  on_delete=models.CASCADE)


class PatientDiagnostic(models.Model):
    diagnostic_date = models.DateField
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)