from django.contrib import admin
from recipes.models import (
    Recipe,
    Tag,
    TagRecipe,
    RecipeIngredient
)


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0


class TagRecipeInline(admin.StackedInline):
    model = TagRecipe
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'favorite_count'
    )

    list_filter = (
        'name',
        'author',
        'tags'
    )

    inlines = [RecipeIngredientInline, TagRecipeInline]

    @admin.display(description="В избранном")
    def favorite_count(self, obj):
        return obj.favorite_recipe.count()


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)

admin.site.empty_value_display = 'Не задано'
