from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers

from medical_history.views import AppointmentViewSet, PatientViewSet

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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include(patient_router.urls)),
]
