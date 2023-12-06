from djoser.serializers import (
    UserSerializer,
    UserCreateSerializer,
)
from rest_framework import serializers
from rest_framework.validators import (
    UniqueValidator,
    UniqueTogetherValidator
)
from authors.models import AuthorSubscriber
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomCreateUserSerializer(UserCreateSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')
        write_only = ('password', )


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class SubscriberSerializer(serializers.ModelSerializer):
    subscriber = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = AuthorSubscriber
        fields = ('subscriber', 'author')

        validators = [
            UniqueTogetherValidator(
                queryset=AuthorSubscriber.objects.all(),
                fields=('subscriber', 'author')
            )
        ]
