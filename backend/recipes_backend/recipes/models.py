from django.db import models
from django.contrib.auth import get_user_model
from ingredients.models import Ingredient

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=16)
    slug = models.SlugField()
    color = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=16)
    description = models.TextField()
    author = models.ForeignKey(
        User, related_name='recipes',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='cats/images/',
        null=True,
        default=None
    )
    tags = models.ManyToManyField(Tag,
                                  through='TagRecipe', related_name='tag_recipe')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient', related_name='ingredient_recipe')
    time = models.IntegerField(verbose_name='Cook time')

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f'Recipe {self.recipe} with Tag {self.tag}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingedient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f'Recipe {self.recipe} with ingedient {self.ingedient}'
