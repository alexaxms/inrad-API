from django.urls import include, path
from rest_framework_nested import routers

from medical_history.views import AppointmentViewSet, PatientViewSet, TreatmentSessionViewSet, DiseaseViewSet, \
    DiseaseTypeViewSet, DiseaseStageViewSet, TreatmentViewSet, TreatmentCategoryViewSet

router = routers.SimpleRouter()
router.register('patients', PatientViewSet)
router.register('diseases', DiseaseViewSet)
router.register('disease_types', DiseaseTypeViewSet)
router.register('disease_stages', DiseaseStageViewSet)
router.register('treatments', TreatmentViewSet)
router.register('treatment_categories', TreatmentCategoryViewSet)

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
