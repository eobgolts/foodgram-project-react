from django.contrib.auth.models import AbstractUser
from django.db import models


class Author(AbstractUser):
    subscribes = models.ManyToManyField("Author", through='AuthorSubscriber', related_name='followers')


class AuthorSubscriber(models.Model):
    subscriber = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='following')

    class Meta:
        ordering = 'author',

    def __str__(self):
        return f'User {self.subscriber} follows {self.author}'
