from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import (
    UniqueTogetherValidator
)

from authors.models import AuthorSubscriber
from authors.serializers import CustomUserSerializer
from recipes.serializers import RecipeSubscriberSerializer

User = get_user_model()


class CustomUserSubscriberSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj) -> int:
        return obj.recipes.count()

    def get_recipes(self, obj) -> list:
        limit = self.context['request'].GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]

        return RecipeSubscriberSerializer(recipes, many=True, read_only=True).data


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
