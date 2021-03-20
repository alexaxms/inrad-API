from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from users.models import User, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class DetailUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name', required=False)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "role")

    def validate_password(self, value: str) -> str:
        return make_password(value)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "role", "password")

    def validate_password(self, value: str) -> str:
        return make_password(value)


class CustomJWTPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class CustomJWTRefreshSerializer(TokenRefreshSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token