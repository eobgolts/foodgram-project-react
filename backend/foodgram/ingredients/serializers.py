from rest_framework import serializers

from ingredients.models import Ingredient, IngredientValue, IngredientMeasurementUnit


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.SlugRelatedField(default=IngredientMeasurementUnit.objects.all(),
                                                    slug_field='measurement_unit',
                                                    read_only=True)

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class IngredientValueSerializer(IngredientSerializer):
    # name = serializers.SlugRelatedField(default=Ingredient.objects.all(),
    #                                     slug_field='name',
    #                                     read_only=True)
    # measurement_unit = serializers.SlugRelatedField

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('name', 'measurement_unit')
        model = IngredientValue
