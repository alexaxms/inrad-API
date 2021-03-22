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

urlpatterns = [
    path("", include(router.urls)),
    path("", include(patient_router.urls)),
]
