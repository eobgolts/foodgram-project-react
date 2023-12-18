from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.validators import (
    UniqueTogetherValidator
)
from authors.serializers import CustomUserSerializer
from ingredients.models import IngredientValue, Ingredient
from ingredients.serializers import IngredientValueSerializer
from recipes.models import RecipeIngredient, Recipe, TagRecipe, UserFavorite, ShoppingCart
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
    ingredients = IngredientValueSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    image = serializers.CharField()
    cooking_time = serializers.IntegerField(min_value=1)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'author', 'image', 'text', 'cooking_time', 'ingredients', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def create(self, validated_data):
        instance = Recipe.objects.create(**validated_data)

        self.write_tag_to_recipes(instance, self.initial_data.get('tags'))
        self.write_ingredients_to_recipes(instance, self.initial_data.get('ingredients'))

        return instance

    def update(self, instance, validated_data):
        self.write_tag_to_recipes(instance, self.initial_data.get('tags'))
        self.write_ingredients_to_recipes(instance, self.initial_data.get('ingredients'))

        return super().update(instance, validated_data)

    def write_tag_to_recipes(self, recipe: Recipe, tags: list[int]) -> None:
        tags_to_write = []
        if not tags:
            raise serializers.ValidationError('Список тегов не может быть пустым')
        for tag in tags:
            try:
                tag_obj = Tag.objects.get(id=tag)
            except ObjectDoesNotExist:
                raise serializers.ValidationError(f'Tag {tag} не существует')
            tags_to_write.append(tag_obj)
        tag_recipe = TagRecipe.objects.filter(recipe=recipe)
        if tag_recipe:
           tag_recipe.delete()

        TagRecipe.objects.bulk_create([TagRecipe(
            tag=tag_obj,
            recipe=recipe
        ) for tag_obj in tags_to_write])

    def write_ingredients_to_recipes(self, recipe: Recipe, ingredients_data: list[dict]):
        ingredients_to_write = []
        if not ingredients_data:
            raise serializers.ValidationError('Список ингредиентов не может быть пустым')
        for ingredient_value in ingredients_data:
            try:
                ingredient = Ingredient.objects.get(id=ingredient_value['id'])
            except ObjectDoesNotExist:
                raise serializers.ValidationError(f'Ингредиент с id {ingredient_value["id"]} не существует')
            else:
                ingredient_value_obj, status = IngredientValue.objects.get_or_create(
                    name=ingredient.name,
                    amount=ingredient_value['amount'],
                    measurement_unit=ingredient.measurement_unit
                )
                ingredients_to_write.append(ingredient_value_obj)
        recipe_ingredient = RecipeIngredient.objects.filter(recipe=recipe)
        if recipe_ingredient:
            recipe_ingredient.delete()
        RecipeIngredient.objects.bulk_create(
            [
            RecipeIngredient(recipe=recipe, ingredient=ingredient_obj)
                for ingredient_obj in ingredients_to_write
            ]
        )

    def get_is_favorited(self, obj) -> bool:
        user = self.context['request'].user

        if user.is_anonymous:
            return False

        return bool(obj.favorite_recipe.filter(user=user))

    def get_is_in_shopping_cart(self, obj) -> bool:
        user = self.context['request'].user

        if user.is_anonymous:
            return False

        return bool(obj.in_user_cart.filter(user=user))


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


class ShoppingCartSerializer(RecipeFavoriteSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe')
            )
        ]
