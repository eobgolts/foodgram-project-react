from django.db.models import (
    QuerySet,
    Model
)
from django.shortcuts import get_object_or_404


def query_with_filter(model: Model,
                      filter_dict: dict,
                      single=False) -> QuerySet:
    if single:
        return get_object_or_404(
            model,
            **filter_dict
        )
    else:
        return model.objects.filter(
            **filter_dict
        )
