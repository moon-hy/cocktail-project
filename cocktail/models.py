from django.db import models

# Create your models here.
COCKTAIL_BASE = (
    'gin',
    'rum',
    'vodka',
    'whiskey'
    'brandy',
    'tequila',
    'wine',
    'mixed',
)
RECIPE_UNIT = (
    'ml',
    'oz',
    'dashes',
    'drops',
    'fill-up',
    'leaves',
)
class Tag(models.Model):
    name = models.CharField(max_length=255)

class Recipe(models.Model):
    UNIT_CHOICES = [
        (i+1, base) for i, base in enumerate(RECIPE_UNIT)
    ]
    cocktail = models.ForeignKey(
        'Cocktail',
        related_name='recipe',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        'ingredient.Ingredient',
        related_name='recipe',
        on_delete=models.CASCADE
    )
    volume = models.PositiveSmallIntegerField()
    unit = models.PositiveSmallIntegerField(choices=UNIT_CHOICES)

class Cocktail(models.Model):
    BASE_CHOICES = [
        (i+1, base) for i, base in enumerate(COCKTAIL_BASE)
    ]
    name = models.CharField(max_length=255)
    base = models.PositiveSmallIntegerField(choices=BASE_CHOICES)
    garnish = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.ManyToManyField(
        'ingredient.Ingredient',
        through='Recipe',
        related_name='cocktails'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='cocktails',
    )
