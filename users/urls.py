from django.urls import path, include
from rest_framework_nested import routers

from .views import set_csrf_token, login_view, UserViewSet, RoleViewSet

router = routers.SimpleRouter()
router.register('users', UserViewSet)
router.register('roles', RoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('set-csrf/', set_csrf_token, name='Set-CSRF'),
    path('login/', login_view, name='Login'),
]
