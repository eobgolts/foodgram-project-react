from django.forms import MultipleChoiceField
from django_filters import rest_framework as filters

from recipes.models import Recipe


class NonValidatingMultipleChoiceField(MultipleChoiceField):
    def validate(self, value):
        pass


class NonValidateChoices(filters.AllValuesMultipleFilter):
    field_class = NonValidatingMultipleChoiceField


class RecipeFilter(filters.FilterSet):
    tags = NonValidateChoices(field_name='tags__slug')
    is_in_shopping_cart = filters.BooleanFilter(method='check_cart')
    is_favorited = filters.BooleanFilter(method='check_favorited')

    def check_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(in_user_cart__user=self.request.user)

        return queryset

    def check_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite_recipe__user=self.request.user)

        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_in_shopping_cart', 'is_favorited']
