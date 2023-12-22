import csv
from pathlib import Path
from django.http import HttpResponse

from django.db.models import QuerySet


def make_file_ready(recipes: QuerySet, filepath: Path) -> HttpResponse:
    recipes_dict: dict = calc_recipes_dict(recipes)

    if filepath.exists():
        filepath.unlink()

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition':
                     f'attachment; filename="{filepath.resolve()}"'},
    )
    fieldnames = ['name', 'measurement_unit', 'amount']
    writer = csv.DictWriter(response, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(recipes_dict.values())

    return response


def calc_recipes_dict(carts: QuerySet) -> dict:
    recipes_dict: dict = {}
    for cart in carts:
        ingredients = cart.recipe.ingredients.all()
        for ingredient in ingredients:
            if recipes_dict.get(ingredient.name):
                recipes_dict[ingredient.name]['amount'] += ingredient.amount
            else:
                recipes_dict[ingredient.name] = {
                    'name': ingredient.name,
                    'measurement_unit':
                        ingredient.measurement_unit.measurement_unit,
                    'amount': ingredient.amount
                }

    return recipes_dict
