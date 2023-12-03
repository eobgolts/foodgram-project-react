from django.db import models
from django.utils.translation import gettext_lazy as _


# class MeasurementUnitChoice(models.TextChoices):
#     TBP = "ст. л.", _("Столовая ложка")
#     TEP = "ч. л.", _("Чайная ложка")
#     ML = "мл", _("Миллилитр")
#     L = 'л', _('Литр')
#     DROP = 'капля', _('Капля')
#     G = 'г', _('Грамм')
#     KG = 'кг', _('Килограмм')
#     THING = 'шт', _('Штука')
#     CUP = 'стакан', _('Стакан')
#     JAR = 'банка', _('Банка')
#     BOTTLE = 'бутылка', _('Бутылка')
#     SMALLBAG = 'пакетик', _('Пакетик')
#     PACK = 'упаковка', _('Упаковка')
#     PACKAGE = 'пакет', _('Пакет')
#     STAR = 'звездочка', _('Звездочка')
#     PINCH = 'щепотка', _('Щепотка')
#     PEACE = 'кусок', _('Кусок')
#     HANDFUL = 'горсть', _('Горсть')
#     BUNCH = 'пучок', _('Пучок')
#     SEGMENT = 'долька', _('Долька')


class Ingredient(models.Model):
    name = models.CharField(max_length=16)
    measurement_unit = models.CharField(max_length=16)


class IngridientValue(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    value = models.IntegerField()


# по вкусу
# зубчик
# пласт
# пачка
# тушка
# стручок
# веточка
# батон
# лист
# стебель

