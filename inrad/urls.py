from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers

from medical_history.views import AppointmentViewSet, PatientViewSet, TreatmentSessionViewSet

router = routers.SimpleRouter()
router.register('patients', PatientViewSet)

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
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include(patient_router.urls)),
]
