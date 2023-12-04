from djoser.serializers import (
    UserSerializer,
    UserCreateSerializer,
)
from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class CustomCreateUserSerializer(UserCreateSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')
        write_only = ('password', )


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
