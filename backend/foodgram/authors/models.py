from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class AuthorSubscriber(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='follower')
    subscribed = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='following')

    class Meta:
        ordering = 'subscriber',

    def __str__(self):
        return f'User {self.subscriber} follows {self.subscribed}'
