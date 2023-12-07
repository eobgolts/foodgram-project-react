from rest_framework import (
    viewsets,
    permissions,
    filters
)

from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer


class IngredientSearch(filters.SearchFilter):
    search_param = 'name'


class IngridientViewSet(viewsets.ReadOnlyModelViewSet):
    model = Ingredient
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (IngredientSearch,)
    search_fields = ('^name',)
    ordering_fields = ('name',)
    pagination_class = None
