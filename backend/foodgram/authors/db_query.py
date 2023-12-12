from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from authors.models import AuthorSubscriber

User = get_user_model()


def query_subscribers(user: User):
    authors = AuthorSubscriber.objects.only('author').filter(subscriber=user)

    return authors


def user_by_id(user: int):
    return get_object_or_404(User, pk=user)
