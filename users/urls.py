from django.urls import path, include
from rest_framework_nested import routers

from .views import UserViewSet, RoleViewSet, CustomJWTPairView, CustomJWTRefreshView

router = routers.SimpleRouter()
router.register("users", UserViewSet)
router.register("roles", RoleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token/", CustomJWTPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomJWTRefreshView.as_view(), name="token_refresh"),
]
