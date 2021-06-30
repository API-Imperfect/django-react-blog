import re

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetConfirmSerializer
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, ValidationError
from django.db import transaction
from rest_framework import serializers

from .error_messages import errors

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(
        required=True,
        min_length=5,
        max_length=20,
        error_messages={
            "required": errors["username"]["required"],
            "blank": errors["username"]["blank"],
            "invalid": errors["username"]["invalid"],
            "min_length": errors["username"]["min_length"],
            "max_length": errors["username"]["max_length"],
        },
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": errors["email"]["required"],
            "blank": errors["email"]["blank"],
            "invalid": errors["email"]["invalid"],
        },
    )
    password1 = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        validators=[
            RegexValidator(
                regex="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).+$",
                message=errors["password1"]["weak_password"],
            )
        ],
        error_messages={
            "max_length": errors["password1"]["max_length"],
            "min_length": errors["password1"]["min_length"],
            "blank": errors["password1"]["blank"],
            "required": errors["password1"]["required"],
        },
    )

    def validate_email(self, email):
        norm_email = email.lower()
        if User.objects.filter(email=norm_email).exists():
            raise ValidationError(errors["email"]["unique"])
        return norm_email

    def validate_username(self, username):
        username_regex = "^(?=.{5,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"

        if not re.match(username_regex, username):
            raise ValidationError(errors["username"]["invalid"])

        if User.objects.filter(username=username.lower()).exists():
            raise ValidationError(errors["username"]["unique"])
        return username.lower()

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.username = self.data.get("username")
        user.email = self.data.get("email")
        user.password1 = self.data.get("password1")
        user.save()
        return user


class CustomPasswordResetSerializer(PasswordResetConfirmSerializer):
    new_password1 = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        validators=[
            RegexValidator(
                regex="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).+$",
                message=errors["new_password1"]["weak_password"],
            )
        ],
        error_messages={
            "max_length": errors["new_password1"]["max_length"],
            "min_length": errors["new_password1"]["min_length"],
            "blank": errors["new_password1"]["blank"],
            "required": errors["new_password1"]["required"],
        },
    )

    @transaction.atomic
    def save(self):
        return self.set_password_form.save()
