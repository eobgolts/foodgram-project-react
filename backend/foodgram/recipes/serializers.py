from rest_framework import serializers
from recipes.models import Tag, Recipe
from rest_framework.validators import (
    UniqueTogetherValidator
)
from ingredients.serializers import IngredientValueSerializer, IngredientSerializer
from authors.serializers import CustomUserSerializer
from ingredients.models import IngredientValue, Ingredient, IngredientMeasurementUnit
from recipes.models import RecipeIngredient, Recipe, TagRecipe
from django.shortcuts import get_object_or_404


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


class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientValueSerializer(many=True)
    tags = TagSerializer(many=True, read_only=True)
    image = serializers.CharField()
    cooking_time = serializers.IntegerField(min_value=1)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'author', 'image', 'text', 'cooking_time', 'ingredients', 'tags')

    def create(self, validated_data):
        ingredients_data = self.initial_data.pop('ingredients')
        tags = self.initial_data.pop('tags')

        validated_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)
        self.write_tag_to_recipes(recipe, tags)
        for ingredient_value in ingredients_data:
            ingredient = get_object_or_404(Ingredient, id=ingredient_value['id'])
            ingredient_value_obj, status = IngredientValue.objects.get_or_create(
                name=ingredient.name,
                amount=ingredient_value['amount'],
                measurement_unit=ingredient.measurement_unit
            )
            RecipeIngredient.objects.create(
                recipe=recipe, ingredient=ingredient_value_obj
            )

        return recipe

    def write_tag_to_recipes(self, recipe: Recipe, tags: list[int]) -> None:
        for tag in tags:
            tag_obj = get_object_or_404(Tag, id=tag)
            TagRecipe.objects.create(
                tag=tag_obj,
                recipe=recipe
            )


class RecipeSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
