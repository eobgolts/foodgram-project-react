from django_filters import rest_framework as filters
from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    #tags = filters.(field_name='recipe_tag__tag', lookup_expr='contains')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def my_custom(self, qs, name, value):
        print(qs)
        print(name)
        if value:
            print('Helllooowefwefwefwe')
            print(value)
            print(qs)

            return qs.filter(recipe_tag__tag__slug=value)
        return qs
