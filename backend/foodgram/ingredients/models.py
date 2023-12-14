from django.db import models


class IngredientMeasurementUnit(models.Model):
    measurement_unit = models.CharField(max_length=16)

    def __str__(self) -> str:
        return f'{self.measurement_unit}'


class Ingredient(models.Model):
    name = models.CharField(max_length=16)
    measurement_unit = models.ForeignKey(IngredientMeasurementUnit, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name}'


class IngredientValue(Ingredient):
    amount = models.IntegerField()
