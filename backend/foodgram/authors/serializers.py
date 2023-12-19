from django.contrib.auth import get_user_model
from djoser.serializers import (
    UserSerializer,
    UserCreateSerializer,
)
from rest_framework import serializers
from rest_framework.validators import (
    UniqueValidator,
)

User = get_user_model()


class CustomCreateUserSerializer(UserCreateSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'password'
                  )
        write_only = ('password', )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj) -> bool:
        user = self.context['request'].user

        if user.is_anonymous:
            return False

        return bool(obj.following.filter(subscriber=user))
