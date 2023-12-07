from __future__ import annotations
from django.contrib.auth import get_user_model
from authors.serializers import SubscriberSerializer
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


User = get_user_model()


class CustomUserViewset(UserViewSet):

    @action(["post"], detail=True)
    def subscribe(self, request, *args, **kwargs) -> Response:
        author = self.get_object()
        subscribe_serializer = SubscriberSerializer(
            data={'subscriber': request.user.id, 'subscribed': author.id}, context={'request': request}
        )
        subscribe_serializer.is_valid(raise_exception=True)
        subscribe_serializer.save()

        serializer = self.serializer_class(instance=author, context={'request': request})

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
