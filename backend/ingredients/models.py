from django.db import models


class IngredientMeasurementUnit(models.Model):
    measurement_unit = models.CharField(
        max_length=16, verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self) -> str:
        return f'{self.measurement_unit}'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=16, verbose_name='Имя ингредиента'
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
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
