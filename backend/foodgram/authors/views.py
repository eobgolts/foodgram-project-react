from __future__ import annotations

from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from authors.subscribe_serializers import SubscriberSerializer, CustomUserSubscriberSerializer

User = get_user_model()


class CustomUserViewset(UserViewSet):

    def get_serializer_class(self):
        if self.action in ('subscribe', 'subscriptions'):
            return CustomUserSubscriberSerializer

        return super().get_serializer_class()

    @action(["post"], detail=True)
    def subscribe(self, request, *args, **kwargs) -> Response:
        author = self.get_object()
        subscribe_serializer = SubscriberSerializer(
            data={'subscriber': request.user.id, 'subscribed': author.id}, context={'request': request}
        )
        subscribe_serializer.is_valid(raise_exception=True)
        subscribe_serializer.save()

        serializer = self.get_serializer(author)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(["get"], detail=False)
    def subscriptions(self, request, *args, **kwargs) -> Response:
        author = request.user
        queryset = User.objects.filter(following__subscriber=author)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
