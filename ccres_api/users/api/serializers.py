from django.contrib.auth import get_user_model
from rest_framework import serializers
from social_django.models import UserSocialAuth

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


class UserSocialAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocialAuth
        fields = "__all__"
