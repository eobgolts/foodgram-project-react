from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class AuthorSubscriber(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    subscribed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        ordering = 'subscriber',

    def __str__(self):
        return f'User {self.subscriber} follows {self.subscribed}'


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_user')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorite_recipe')

    def __str__(self):
        return f'User {self.user} favorite {self.recipe}'
