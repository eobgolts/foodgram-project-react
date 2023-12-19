from django.core.management.base import BaseCommand

from recipes.models import Tag

COLOR_HEX_LIST = ['#FF0000', '#0000FF', '#008000', '#FFFF00', '#000000']


class Command(BaseCommand):
    help = "Предзагрузка списка тегов"

    def handle(self, *args, **options):
        Tag.objects.bulk_create(
            [Tag(
                name=f'Tag{idx}',
                slug=f'tag{idx}',
                color=color
            ) for idx, color in enumerate(COLOR_HEX_LIST)])
