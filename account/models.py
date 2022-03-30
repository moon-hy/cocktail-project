from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE
    )
    favorites   = models.ManyToManyField(
        'cocktail.Cocktail',
        related_name='favorited',
        blank=True,
    )
    shelf        = models.ManyToManyField(
        'ingredient.Ingredient',
        related_name='+',
        blank=True,
    )
    
    def __str__(self):
        return self.user.username
        
    def favorite(self, cocktail):
        self.favorites.add(cocktail)

    def unfavorite(self, cocktail):
        self.favorites.remove(cocktail)
    
    def is_favorited(self, cocktail):
        return self.favorites.filter(pk=cocktail.pk).exists()
    
    def shelve(self, ingredient):
        self.shelf.add(ingredient)

    def unshelve(self, ingredient):
        self.shelf.remove(ingredient)

    def is_shelved(self, ingredient):
        return self.shelf.filter(pk=ingredient.pk).exists()
