from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=16)
    measurement_unit = models.CharField(max_length=16)


class IngredientValue(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()
