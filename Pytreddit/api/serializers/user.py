from rest_framework import serializers

from users.models import Profile


# Class ProfileSerializer extends
# django_rest_framework serializers model
# Is a serializer for Profile objects
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "login",
            "username",
            "password",
            "phone",
            "profile_link",
            "profile_picture_name",
        )
