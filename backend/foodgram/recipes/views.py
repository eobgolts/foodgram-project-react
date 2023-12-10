from rest_framework import (
    viewsets,
    permissions,
)

from recipes.models import Tag, Recipe
from recipes.serializers import TagSerializer, RecipesSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    model = Tag
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )