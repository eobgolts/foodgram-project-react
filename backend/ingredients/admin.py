from django.contrib import admin
from ingredients.models import (
    Ingredient,
    IngredientMeasurementUnit,
    IngredientValue
)


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientMeasurementUnit)
admin.site.register(IngredientValue)

admin.site.empty_value_display = 'Не задано'
