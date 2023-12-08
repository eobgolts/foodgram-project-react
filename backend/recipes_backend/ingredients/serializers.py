from rest_framework import serializers

from ingredients.models import Ingredient, IngridientValue


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class IngredientValueSerializer(serializers.ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(source='id')

    class Meta:
        fields = ('ingridient', 'amount')
        model = IngridientValue
