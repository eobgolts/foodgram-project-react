from rest_framework import status
from rest_framework import (
    viewsets
)
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from recipes.models import Tag, Recipe, ShoppingCart, UserFavorite
from rest_framework.exceptions import MethodNotAllowed

from recipes.serializers import TagSerializer, RecipesSerializer, RecipeSubscriberSerializer, RecipeFavoriteSerializer, \
    ShoppingCartSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    model = Tag
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )

    def perform_update(self, serializer):
        if self.request.method == 'PUT':
            raise MethodNotAllowed(self.request.method)

        serializer.save(
            author=self.request.user,
        )

    def get_serializer_class(self):
        if self.action in ['favorite', 'shopping_cart']:
            return RecipeSubscriberSerializer

        return super().get_serializer_class()

    @action(["post", "delete"], detail=True)
    def favorite(self, request, *args, **kwargs) -> Response:
        return self.work_with_favorite_or_cart(request, RecipeFavoriteSerializer, UserFavorite)

    @action(["post", "delete"], detail=True)
    def shopping_cart(self, request, *args, **kwargs) -> Response:
        return self.work_with_favorite_or_cart(request, ShoppingCartSerializer, ShoppingCart)

    def work_with_favorite_or_cart(self, request, serializer, model) -> Response:
        recipe = self.get_object()

        if request.method == "DELETE":
            try:
                instance = model.objects.get(user=request.user.id, recipe=recipe)
                self.perform_destroy(instance)
            except Exception as exc:
                raise ValidationError(exc)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        write_serializer = serializer(
            data={'user': request.user.id, 'recipe': recipe.id}, context={'request': request}
        )
        write_serializer.is_valid(raise_exception=True)
        write_serializer.save()
        serializer = self.get_serializer(recipe)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
