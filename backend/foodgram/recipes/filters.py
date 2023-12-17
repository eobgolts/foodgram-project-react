from django_filters import rest_framework as filters
from recipes.models import Recipe, ShoppingCart


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_in_shopping_cart = filters.BooleanFilter(method='check_cart')

    def check_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(in_user_cart__user=self.request.user)

        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_in_shopping_cart']
