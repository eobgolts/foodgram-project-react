from rest_framework import serializers

from ingredients.models import (
    Ingredient,
    IngredientValue,
    IngredientMeasurementUnit
)


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.SlugRelatedField(
        default=IngredientMeasurementUnit.objects.all(),
        slug_field='measurement_unit',
        read_only=True
    )

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class IngredientValueSerializer(IngredientSerializer):
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('name', 'measurement_unit')
        model = IngredientValue
