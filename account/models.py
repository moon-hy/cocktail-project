from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    fav_ingredients = models.ManyToManyField(
        'ingredient.Ingredient',
        related_name='favorited'
    )
    fav_cocktails= models.ManyToManyField(
        'cocktail.Cocktail',
        related_name='favorited'
    )
    ingredients= models.ManyToManyField(
        'ingredient.Ingredient',
        related_name='+'
    )
