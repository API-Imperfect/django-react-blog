from blog.settings.base import AUTH_USER_MODEL
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from apps.profiles.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="get_username")

    class Meta:
        model = UserProfile
        fields = [
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "gender",
        ]
        read_only_fields = ["created_at", "updated_at"]


class UserSerializer(UserDetailsSerializer):
    profile = UserProfileSerializer(source="userprofile")

    class Meta(UserDetailsSerializer.Meta):
        fields = ["email", "profile"]

    def update(self, instance, validated_data):
        userprofile_serializer = self.fields["profile"]
        userprofile_instance = instance.userprofile
        userprofile_data = validated_data.pop("userprofile", {})
        userprofile_serializer.update(userprofile_instance, userprofile_data)

        instance = super().update(instance, validated_data)

        return instance
