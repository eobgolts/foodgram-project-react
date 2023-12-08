import json

from django.core.management.base import BaseCommand
from ingredients.models import Ingredient
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

        Ingredient.objects.bulk_create([Ingredient(**_) for _ in file_content])
