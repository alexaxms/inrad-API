from django.urls import include, path
from rest_framework_nested import routers

from medical_history.views import AppointmentViewSet, PatientViewSet, TreatmentSessionViewSet, DiseaseViewSet, \
    DiseaseTypeViewSet, DiseaseStageViewSet

router = routers.SimpleRouter()
router.register('patients', PatientViewSet)
router.register('diseases', DiseaseViewSet)
router.register('disease_types', DiseaseTypeViewSet)
router.register('disease_stages', DiseaseStageViewSet)

patient_router = routers.NestedSimpleRouter(
    router,
    r'patients',
    lookup='patient')
patient_router.register(
    r'appointments',
    AppointmentViewSet,
    basename='patient-appointments'
)
patient_router.register(
    r'treatment_session',
    TreatmentSessionViewSet,
    basename='patient-treatment_sessions'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(patient_router.urls)),
]