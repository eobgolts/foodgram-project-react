from rest_framework import serializers
from recipes.models import Tag, Recipe
from rest_framework.validators import (
    UniqueTogetherValidator
)
from ingredients.serializers import IngredientValueSerializer


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
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    image = serializers.CharField(max_length=100)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'author', 'image', 'text', 'cooking_time', 'ingredients', 'tags')





'''
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
                                  through='TagRecipe')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient')
    time = models.IntegerField(verbose_name='Cook time')

    def __str__(self):
        return self.name
'''