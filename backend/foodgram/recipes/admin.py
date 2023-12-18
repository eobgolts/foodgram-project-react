from django.contrib import admin
from recipes.models import (
    Recipe,
    Tag,
    RecipeIngredient
)


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author'
    )

    list_filter = (
        'name',
        'author',
        'tags'
    )

    inlines = [RecipeIngredientInline,]

    def favorite_count(self, obj):
        return self.obj.favorite_recipe.count()


admin.site.register(Recipe, RecipeAdmin)

admin.site.empty_value_display = 'Не задано'
