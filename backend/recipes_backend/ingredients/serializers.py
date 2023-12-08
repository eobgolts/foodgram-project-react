from rest_framework import serializers

from ingredients.models import Ingredient, IngredientValue


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class IngredientValueSerializer(serializers.ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(source='id', queryset=Ingredient.objects.all())

    class Meta:
        fields = ('ingredient', 'amount')
        model = IngredientValue
