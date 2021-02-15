from django.contrib.auth.hashers import make_password
from rest_framework import serializers

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
        fields = ("id", "username", "first_name", "last_name", "email", "role")

    def validate_password(self, value: str) -> str:
        return make_password(value)
