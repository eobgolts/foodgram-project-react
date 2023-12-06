from django.db.models import (
    QuerySet,
    Model
)
from django.shortcuts import get_object_or_404
from authors.models import AuthorSubscriber
from django.contrib.auth import get_user_model

User = get_user_model()


def query_subscribers(user: User):
    authors = AuthorSubscriber.objects.only('author').filter(subscriber=user)

    return authors


def user_by_id(user: str):
    print(user)
    return get_object_or_404(User, username=user)
