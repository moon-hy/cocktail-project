from unicodedata import name
from django.db import models


COCKTAIL_BASE = (
    'gin',
    'rum',
    'vodka',
    'whiskey',
    'brandy',
    'tequila',
    'wine',
    'mixed',
)
COCKTAIL_GLASS = (
    'any',
    'hot-drink', 
    'collins', 
    'highball', 
    'martini', 
    'hurricane', 
    'white-wine', 
    'old-fashioned', 
    'margarita', 
    'shot', 
    'champagne-tulip', 
    'champagne-flute'
)
RECIPE_UNIT = (
    'ml',
    'oz',
    'dashes',
    'drops',
    'fill-up',
    'bsp',
    'leaves',
    'slices',
    'parts',
)
class SimpleModel(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

class Tag(SimpleModel):
    pass

class Base(SimpleModel):
    pass

class Method(SimpleModel):
    pass

class Recipe(models.Model):
    UNIT_CHOICES = [
        (i+1, base) for i, base in enumerate(RECIPE_UNIT)
    ]
    cocktail    = models.ForeignKey(
        'Cocktail',
        related_name='recipe',
        on_delete=models.CASCADE,
        blank=True
    )
    ingredient  = models.ForeignKey(
        'ingredient.Ingredient',
        related_name='recipe',
        on_delete=models.CASCADE
    )
    volume      = models.PositiveSmallIntegerField()
    unit        = models.PositiveSmallIntegerField(choices=UNIT_CHOICES)
    optional    = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.cocktail.name} <- {self.ingredient.name}'

class Cocktail(models.Model):
    GLASS_CHOICES = [
        (i+1, glass) for i, glass in enumerate(COCKTAIL_GLASS)
    ]

    name        = models.CharField(max_length=255)
    base        = models.ForeignKey(
        'Base',
        related_name='cocktails',
        on_delete=models.CASCADE,
    )
    glass       = models.PositiveSmallIntegerField(choices=GLASS_CHOICES, default=1)
    method      = models.ManyToManyField(
        'Method',
        related_name='cocktails',
        blank=True
    )
    garnish     = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    ingredients = models.ManyToManyField(
        'ingredient.Ingredient',
        through='Recipe',
        related_name='cocktails'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='cocktails',
        blank=True
    )
    
    def __str__(self):
        return self.name