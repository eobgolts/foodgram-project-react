from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.conf import settings

from ingredients.models import IngredientValue

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, verbose_name='Slug имя')
    color = models.CharField(max_length=7, verbose_name='Цвет')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug', 'color'],
                name='unique_name_slug_color'
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField(verbose_name='Описание рецепта')
    author = models.ForeignKey(
        User, related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Фото блюда'
    )
    tags = models.ManyToManyField(Tag,
                                  through='TagRecipe',
                                  verbose_name='Тэги рецепта')
    ingredients = models.ManyToManyField(IngredientValue,
                                         through='RecipeIngredient',
                                         verbose_name='Ингредиенты рецепта')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MaxValueValidator(settings.MAX_INTEGER_VALUE),
            MinValueValidator(settings.MIN_INTEGER_VALUE)
        ]
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_tag',
                               verbose_name='Рецепт')
    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE,
                            related_name='tag_recipe',
                            verbose_name='Тэг')

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Тэг - Рецепт'
        verbose_name_plural = 'Тэги - Рецепты'

    def __str__(self):
        return f'Рецепт "{self.recipe}" с тегом "{self.tag}"'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_ingredient',
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(IngredientValue,
                                   on_delete=models.CASCADE,
                                   related_name='ingredient_recipe',
                                   verbose_name='Ингредиент')

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Рецепт - Ингридиент'
        verbose_name_plural = 'Рецепты - Ингридиенты'

    def __str__(self):
        return f'Ингридиент "{self.ingredient}" для рецепта "{self.recipe}"'


class UserFavorite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorite_user',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favorite_recipe',
                               verbose_name='Избранный рецепт')

    class Meta:
        ordering = ('user',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'User {self.user} favorite {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='in_cart',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='in_user_cart',
                               verbose_name='Рецепт в корзине')

    class Meta:
        ordering = ('user',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина покупок'

    def __str__(self):
        return f'User {self.user} shopping cart'
