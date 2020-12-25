from django.contrib import admin

from medical_history.models import Diagnostic, Treatment, Appointment, MedicalAppointmentImage, PatientTreatment, \
    PatientDiagnostic, Patient, PatientAttachmentData, SymptomGroup, Symptom, DiseaseType, DiseaseStage, Disease, \
    TreatmentSession, TreatmentSessionImage

admin.site.register(Diagnostic)
admin.site.register(Treatment)
admin.site.register(Appointment)
admin.site.register(MedicalAppointmentImage)
admin.site.register(PatientTreatment)
admin.site.register(PatientDiagnostic)
admin.site.register(Patient)
admin.site.register(PatientAttachmentData)
admin.site.register(SymptomGroup)
admin.site.register(Symptom)
admin.site.register(DiseaseType)
admin.site.register(DiseaseStage)
admin.site.register(Disease)
admin.site.register(TreatmentSession)
admin.site.register(TreatmentSessionImage)
