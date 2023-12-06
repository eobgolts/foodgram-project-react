from __future__ import annotations
from typing import TYPE_CHECKING

from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin
)
from rest_framework.viewsets import GenericViewSet
from authors.db_query import query_subscribers, user_by_id
from django.contrib.auth import get_user_model
from authors.serializers import CustomUserSerializer, SubscriberSerializer

if TYPE_CHECKING:
    from django.db.models import (
        QuerySet
    )


User = get_user_model()


class SubscriptionListViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = CustomUserSerializer

    def get_queryset(self) -> QuerySet:
        return query_subscribers(self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            subscriber=self.request.user,
        )


class SubscriptionViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):

    def perform_create(self, serializer):
        serializer.save(
            subscriber=self.request.user,
            author=user_by_id(self.kwargs.get('user_id'))
        )

    def get_serializer_class(self):
        if self.action == 'create':
            print('111111111111111')
            return SubscriberSerializer

        return CustomUserSerializer
