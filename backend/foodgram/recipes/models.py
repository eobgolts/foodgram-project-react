from django.contrib.auth import get_user_model
from django.db import models

from ingredients.models import IngredientValue

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=16)
    slug = models.SlugField()
    color = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(
        User, related_name='recipes',
        on_delete=models.CASCADE
    )
    image = models.TextField()
    tags = models.ManyToManyField(Tag,
                                  through='TagRecipe')
    ingredients = models.ManyToManyField(IngredientValue,
                                         through='RecipeIngredient')
    cooking_time = models.PositiveIntegerField(verbose_name='Cook time')

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_tag')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag_recipe')

    def __str__(self):
        return f'Recipe {self.recipe} with Tag {self.tag}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(IngredientValue, on_delete=models.CASCADE)

    def __str__(self):
        return f'Recipe {self.recipe} with ingedient {self.ingedients}'


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_user')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorite_recipe')

    def __str__(self):
        return f'User {self.user} favorite {self.recipe}'


class ShoppingCart(UserFavorite):

    def __str__(self):
        return f'User {self.user} shopping cart'
