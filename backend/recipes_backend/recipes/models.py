from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

INGRIDIENT_MASS_CHOICES = (
        ('tbs', 'ст.л'),
        ('tes', 'ч.л'),
        ('g', 'г'),
        ('ml', 'мл'),
        ('val', 'шт'),
    )


class Tag(models.Model):
    name = models.CharField()
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
                                  through='TagRecipes')
    time = models.IntegerField(verbose_name='Cook time')

    def __str__(self):
        return self.name


class Ingridient(models.Model):
    name = models.CharField()
    value = models.IntegerField()
    value_type = models.Choices(INGRIDIENT_MASS_CHOICES)


class TagRecipes(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f'Recipe {self.recipe} with Tag {self.tag}'
