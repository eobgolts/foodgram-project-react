from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.conf import settings


class IngredientMeasurementUnit(models.Model):
    measurement_unit = models.CharField(
        max_length=200, verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self) -> str:
        return f'{self.measurement_unit}'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Имя ингредиента'
    )
    measurement_unit = models.ForeignKey(
        IngredientMeasurementUnit, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Тип ингредиента'
        verbose_name_plural = 'Типы ингредиентов'

    def __str__(self) -> str:
        return f'{self.name}'


class IngredientValue(Ingredient):
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MaxValueValidator(settings.MAX_INTEGER_VALUE),
            MinValueValidator(settings.MIN_INTEGER_VALUE)
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
