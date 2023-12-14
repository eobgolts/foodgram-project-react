from __future__ import annotations

from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from authors.permissions import AuthorOnly
from authors.models import AuthorSubscriber
from authors.subscribe_serializers import SubscriberSerializer, CustomUserSubscriberSerializer
from recipes.serializers import RecipeSubscriberSerializer

User = get_user_model()


class CustomUserViewset(UserViewSet):

    def get_serializer_class(self):
        if self.action in ('subscribe', 'subscriptions'):
            return CustomUserSubscriberSerializer

        if self.action == 'favorite':
            return RecipeSubscriberSerializer

        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "me":
            self.permission_classes = (AuthorOnly, )

        return super().get_permissions()

    @action(["post", "delete"], detail=True)
    def subscribe(self, request, *args, **kwargs) -> Response:
        author = self.get_object()

        if request.method == "DELETE":
            try:
                instance = AuthorSubscriber.objects.get(subscriber=request.user.id, subscribed=author)
                self.perform_destroy(instance)
            except Exception as exc:
                raise ValidationError(exc)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

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
