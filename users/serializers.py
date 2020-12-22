from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "roles")

    def validate_password(self, value: str) -> str:
        return make_password(value)
