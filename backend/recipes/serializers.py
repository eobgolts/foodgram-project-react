import base64
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.validators import (
    UniqueTogetherValidator
)
from django.conf import settings

from authors.serializers import CustomUserSerializer
from ingredients.models import (
    IngredientValue,
    Ingredient
)
from ingredients.serializers import IngredientValueSerializer
from recipes.models import (
    RecipeIngredient,
    Recipe,
    TagRecipe,
    UserFavorite,
    ShoppingCart
)
from recipes.models import Tag

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


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
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        min_value=settings.MIN_INTEGER_VALUE,
        max_value=settings.MAX_INTEGER_VALUE
    )
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'author', 'image',
                  'text', 'cooking_time', 'ingredients',
                  'tags', 'is_favorited', 'is_in_shopping_cart')

    def create(self, validated_data):

        tags, ingredients = self.validate_ingredients_tags()

        instance: Recipe = Recipe.objects.create(**validated_data)

        self.write_tag_to_recipes(instance, tags)
        self.write_ingredients_to_recipes(instance, ingredients)

        return instance

    def update(self, instance, validated_data):
        tags, ingredients = self.validate_ingredients_tags()

        self.write_tag_to_recipes(instance, tags)
        self.write_ingredients_to_recipes(instance, ingredients)

        return super().update(instance, validated_data)

    def write_tag_to_recipes(self, recipe: Recipe,
                             tags_to_write: list[Tag]) -> None:
        tag_recipe: QuerySet[TagRecipe] = recipe.recipe_tag.all()
        if tag_recipe:
            tag_recipe.delete()
        recipe.recipe_tag.bulk_create([TagRecipe(
            tag=tag_obj,
            recipe=recipe
        ) for tag_obj in tags_to_write])

    def write_ingredients_to_recipes(
            self, recipe: Recipe,
            ingredients_to_write: list[IngredientValue]
    ):
        recipe_ingredient: QuerySet[RecipeIngredient] = (
            recipe.recipe_ingredient.all()
        )
        if recipe_ingredient:
            recipe_ingredient.delete()

        recipe.recipe_ingredient.bulk_create(
            [RecipeIngredient(recipe=recipe,
                              ingredient=ingredient_obj)
                for ingredient_obj in ingredients_to_write]
        )

    def validate_ingredients_tags(self) -> tuple[
        list[Tag],
        list[IngredientValue]
    ]:

        tags = self.initial_data.get('tags')
        tags_to_write: list[Tag] = self.validate_tags(tags)

        ingredients_data = self.initial_data.get('ingredients')
        ingredients_to_write: list[
            IngredientValue
        ] = self.validate_ingredients(
            ingredients_data
        )

        return tags_to_write, ingredients_to_write

    def validate_tags(self, tags_list: list[int]) -> list[Tag]:
        validated_tags: list[Tag] = []

        if not tags_list:
            raise serializers.ValidationError(
                'Список тегов не может быть пустым'
            )
        if len(set(tags_list)) < len(tags_list):
            raise serializers.ValidationError(
                'Список тегов содержит дублирующие значения'
            )
        for tag in tags_list:
            try:
                tag_obj: Tag = Tag.objects.get(id=tag)
            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    f'Tag {tag} не существует'
                )
            validated_tags.append(tag_obj)

        return validated_tags

    def validate_ingredients(self, ingredient_list: list[dict]) -> list[
        IngredientValue
    ]:
        validated_ingredients: list[
            IngredientValue
        ] = []
        if not ingredient_list:
            raise serializers.ValidationError(
                'Список ингредиентов не может быть пустым'
            )

        if len(
                set([d['id'] for d in ingredient_list])
        ) < len(ingredient_list):
            raise serializers.ValidationError(
                'Список ингредиентов содержит дублирующие значения'
            )

        for ingredient_value in ingredient_list:
            serializer = IngredientValueSerializer(data=ingredient_value)
            serializer.is_valid(raise_exception=True)
            try:
                ingredient: Ingredient = Ingredient.objects.get(
                    id=ingredient_value['id']
                )
            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    f'Ингредиент с id {ingredient_value["id"]} '
                    f'не существует'
                )
            else:
                ingredient_value_obj, status = (
                    IngredientValue.objects.get_or_create(
                        name=ingredient.name,
                        amount=ingredient_value['amount'],
                        measurement_unit=ingredient.measurement_unit)
                )
                validated_ingredients.append(ingredient_value_obj)

        return validated_ingredients

    def get_is_favorited(self, obj) -> bool:
        user = self.context['request'].user

        if user.is_anonymous:
            return False

        return obj.favorite_recipe.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj) -> bool:
        user = self.context['request'].user

        if user.is_anonymous:
            return False

        return obj.in_user_cart.filter(user=user).exists()


class RecipeSubscriberSerializer(RecipesSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )

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
