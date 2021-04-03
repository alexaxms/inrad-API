from django.urls import include, path
from rest_framework_nested import routers

from medical_history.views import (
    AppointmentViewSet,
    PatientViewSet,
    DiseaseTypeViewSet,
    TreatmentViewSet,
    TreatmentCategoryViewSet,
    SymptomGroupViewSet,
    SymptomViewSet,
    TreatmentMachineViewSet,
    TreatmentModeViewSet,
    PatientDiagnosticViewSet,
    PatientTreatmentViewSet,
    PatientAttachmentDataViewSet,
    DiseaseCategoryViewSet,
    SymptomByGroupViewSet,
    PatientAppointmentImageViewSet,
)

router = routers.SimpleRouter()
router.register("patients", PatientViewSet)
router.register("disease_categories", DiseaseCategoryViewSet)
router.register("disease_types", DiseaseTypeViewSet)
router.register("treatments", TreatmentViewSet)
router.register("treatment_categories", TreatmentCategoryViewSet)
router.register("treatment_machines", TreatmentMachineViewSet)
router.register("treatment_modes", TreatmentModeViewSet)
router.register("symptom_groups", SymptomGroupViewSet)
router.register("symptoms", SymptomViewSet)

patient_router = routers.NestedSimpleRouter(router, r"patients", lookup="patient")
symptom_group_router = routers.NestedSimpleRouter(
    router, r"symptom_groups", lookup="symptom_group"
)

patient_router.register(
    r"appointments", AppointmentViewSet, basename="patient-appointments"
)

patient_router.register(
    r"diagnostics", PatientDiagnosticViewSet, basename="patient-diagnostics"
)

patient_router.register(
    r"treatments", PatientTreatmentViewSet, basename="patient-treatments"
)

patient_router.register(
    r"attachments", PatientAttachmentDataViewSet, basename="patient-attachments"
)

symptom_group_router.register(
    r"symptoms", SymptomByGroupViewSet, basename="symptoms-by-group"
)

appointment_router = routers.NestedSimpleRouter(
    patient_router, r"appointments", lookup="appointment"
)

appointment_router.register(
    r"images", PatientAppointmentImageViewSet, basename="patient-appointment-images"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(patient_router.urls)),
    path("", include(symptom_group_router.urls)),
    path("", include(appointment_router.urls)),
]
