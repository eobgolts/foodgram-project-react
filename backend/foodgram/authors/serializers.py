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
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj) -> bool:
        user = self.context['request'].user

        if user.is_anonymous:
            return False

        return bool(obj.following.filter(subscriber=user))


class SubscriberSerializer(serializers.ModelSerializer):
    subscriber = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    subscribed = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = AuthorSubscriber
        fields = ('subscriber', 'subscribed')

        validators = [
            UniqueTogetherValidator(
                queryset=AuthorSubscriber.objects.all(),
                fields=('subscriber', 'subscribed')
            )
        ]

    def validate(self, data):
        user = self.context['request'].user

        if user == data['subscribed']:
            raise serializers.ValidationError('Невозможно выполнить '
                                              'подписку пользователя, '
                                              f'{user} на себя самого')

        return data
