from django.contrib import admin

from medical_history.models import Diagnostic, Treatment, Appointment, MedicalAppointmentImage, PatientTreatment, \
    PatientDiagnostic, Patient

admin.site.register(Diagnostic)
admin.site.register(Treatment)
admin.site.register(Appointment)
admin.site.register(MedicalAppointmentImage)
admin.site.register(PatientTreatment)
admin.site.register(PatientDiagnostic)
admin.site.register(Patient)
