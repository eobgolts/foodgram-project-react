from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser)

class AuthorSubscriber(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    subscribed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        ordering = 'subscriber',

    def __str__(self):
        return f'User {self.subscriber} follows {self.subscribed}'
