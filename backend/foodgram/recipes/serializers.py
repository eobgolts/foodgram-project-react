from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import (
    UniqueTogetherValidator
)

from authors.models import UserFavorite
from authors.serializers import CustomUserSerializer
from ingredients.models import IngredientValue, Ingredient
from ingredients.serializers import IngredientValueSerializer
from recipes.models import RecipeIngredient, Recipe, TagRecipe
from recipes.models import Tag

User = get_user_model()


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
    is_favorited = serializers.SerializerMethodField()


    class Meta:
        model = Recipe
        fields = ('id', 'name', 'author', 'image', 'text', 'cooking_time', 'ingredients', 'tags', 'is_favorited')

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

    def get_is_favorited(self, obj) -> bool:
        user = self.context['request'].user

        if user.is_anonymous:
            return False

        return bool(obj.favorite_recipe.filter(user=user))


class RecipeSubscriberSerializer(RecipesSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = UserFavorite
        fields = ('user', 'recipe')

        validators = [
            UniqueTogetherValidator(
                queryset=UserFavorite.objects.all(),
                fields=('user', 'recipe')
            )
        ]
