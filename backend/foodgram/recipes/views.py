from rest_framework import status
from rest_framework import (
    viewsets,
    permissions,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import Tag, Recipe
from recipes.serializers import TagSerializer, RecipesSerializer, RecipeSubscriberSerializer, RecipeFavoriteSerializer


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

    def get_serializer_class(self):
        if self.action == 'favorite':
            return RecipeSubscriberSerializer

        return super().get_serializer_class()

    @action(["post"], detail=True)
    def favorite(self, request, *args, **kwargs) -> Response:
        recipe = self.get_object()
        favorite_serializer = RecipeFavoriteSerializer(
            data={'user': request.user.id, 'recipe': recipe.id}, context={'request': request}
        )
        favorite_serializer.is_valid(raise_exception=True)
        favorite_serializer.save()

        serializer = self.get_serializer(recipe)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
