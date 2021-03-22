from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(unique=True, max_length=40)


class User(AbstractUser):
    ADMIN = "ADMIN"
    USER_TYPES = (
        ("EMPLOYEE", "Employee"),
        ("ADMIN", "Admin"),
    )
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default="Employee")
    role = models.ForeignKey(
        Role, related_name="users", on_delete=models.CASCADE, null=True
    )

    REQUIRED_FIELDS = ("first_name", "last_name", "email", "user_type")

    @property
    def is_admin(self):
        return self.user_type == self.ADMIN

    def to_dict(self) -> dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role.name if self.role else None,
        }
