from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .model_managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    object = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip().title()
