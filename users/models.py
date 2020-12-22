from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = "Admin"
    USER_TYPES = (
        ("Employee", "Employee"),
        ("Admin", "Admin"),
    )
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='Employee')
    roles = models.ManyToManyField('Role')

    REQUIRED_FIELDS = ('first_name', 'last_name', 'email', 'user_type')

    @property
    def is_admin(self):
        return self.user_type == self.ADMIN


class Role(models.Model):
    name = models.CharField(unique=True, max_length=40)
