from django.contrib import admin

from medical_history.models import (
    Treatment,
    Appointment,
    MedicalAppointmentImage,
    PatientTreatment,
    PatientDiagnostic,
    Patient,
    PatientAttachmentData,
    SymptomGroup,
    Symptom,
    DiseaseType,
)

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
