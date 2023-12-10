import json

from django.core.management.base import BaseCommand
from ingredients.models import (
    Ingredient,
    IngredientMeasurementUnit
)
from pathlib import Path


class Command(BaseCommand):
    help = "Предзагрузка списка возможных ингридиентов"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file_path",
            help="Filepath to datafile",
            required=False,
            default=Path(__file__).resolve().parent.parent.parent.parent.parent.parent / 'data' / 'ingredients.json'
        )

    def handle(self, *args, **options):
        with open(options['file_path'], 'r', encoding='UTF-8') as f:
            file_content = json.load(f)
            measure_units = set([k['measurement_unit'] for k in file_content])
            IngredientMeasurementUnit.objects.bulk_create(IngredientMeasurementUnit(measurement_unit=_) for _ in
                                                          measure_units)
            ingredient_dict = {ingred.measurement_unit: ingred
                               for ingred in IngredientMeasurementUnit.objects.all()}

        Ingredient.objects.bulk_create([Ingredient(
            name=_['name'],
            measurement_unit=ingredient_dict[_["measurement_unit"]]
        ) for _ in file_content])