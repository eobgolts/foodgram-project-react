from __future__ import annotations
from typing import TYPE_CHECKING

from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin
)
from rest_framework.viewsets import GenericViewSet
from authors.models import AuthorSubscriber
from authors.db_query import query_with_filter
from django.contrib.auth import get_user_model
from authors.serializers import CustomUserSerializer

if TYPE_CHECKING:
    from django.db.models import (
        QuerySet
    )


User = get_user_model()


class SubscriptionListViewSet(ListModelMixin, GenericViewSet):
    #serializer_class = CustomUserSerializer

    def get_queryset(self) -> QuerySet:
        print('Hellosafsasaggagag')
        # authors = query_with_filter(
        #     AuthorSubscriber, {'subscriber': self.request.user},
        # ).only('author')
        #
        # return authors

    def perform_create(self, serializer):
        serializer.save(
            subscriber=self.request.user,
        )
