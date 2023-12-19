import csv
from pathlib import Path

from django.db.models import QuerySet


def make_file_ready(recipes: QuerySet, filepath: Path) -> None:
    recipes_dict: dict = calc_recipes_dict(recipes)
    if filepath.exists():
        filepath.unlink()
    with open(filepath, 'w', newline='', encoding='UTF-8') as csvfile:
        fieldnames = ['name', 'measurement_unit', 'amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(recipes_dict.values())


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
