from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from users.models import User, Role
from users.serializers import (
    UserSerializer,
    RoleSerializer,
    DetailUserSerializer,
    CustomJWTPairSerializer,
    CustomJWTRefreshSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    filterset_fields = ["username"]
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return DetailUserSerializer
        return UserSerializer


class RoleViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filterset_fields = ["name"]
    permission_classes = (IsAuthenticated,)


class CustomJWTPairView(TokenObtainPairView):
    serializer_class = CustomJWTPairSerializer


class CustomJWTRefreshView(TokenRefreshView):
    serializer_class = CustomJWTRefreshSerializer
