from rest_framework import serializers
from recipes.models import Tag
from rest_framework.validators import (
    UniqueTogetherValidator
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'color')

        validators = [
            UniqueTogetherValidator(
                queryset=Tag.objects.all(),
                fields=('name', 'slug', 'color')
            )
        ]
