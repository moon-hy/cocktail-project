from django.db import models


COCKTAIL_BASE = (
    ('whiskey', 'whiskey'),
    ('vodka', 'vodka'),
    ('rum', 'rum'),
    ('gin', 'gin'),
    ('tequila', 'tequila'),
    ('brandy', 'brandy'),
    ('liqueur', 'liqueur'),
    ('wine', 'wine'),
    ('mixed', 'mixed'),
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

UNIT_CHOICES = (
    ('ml', 'ml'),
    ('dashes','dashes'),
    ('drops','drops'),
    ('bsp','bsp'),
    ('ea','ea'),
    ('slices','slices'),
    ('parts','parts'),
    ('prefers','prefers'),
)

class Tag(models.Model):
    name = models.CharField(max_length=32, primary_key=True)

    def __str__(self):
        return self.name

class Method(models.Model):
    name = models.CharField(max_length=16, primary_key=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
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
    unit        = models.CharField(max_length=16, choices=UNIT_CHOICES)
    optional    = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.cocktail.name} <- {self.ingredient.name}'

class Cocktail(models.Model):
    GLASS_CHOICES = [
        (i+1, glass) for i, glass in enumerate(COCKTAIL_GLASS)
    ]

    name        = models.CharField(max_length=255)
    base        = models.CharField(max_length=32, choices=COCKTAIL_BASE)
    glass       = models.PositiveSmallIntegerField(choices=GLASS_CHOICES, default=1)
    methods     = models.ManyToManyField(
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
    tags        = models.ManyToManyField(
        'Tag',
        related_name='cocktails',
        blank=True
    )
    abv         = models.DecimalField(max_digits=3, decimal_places=1, default=0)

    def save(self, *args, **kwargs):
        self.abv = self.get_abv()
        return super().save(*args, **kwargs)

    def get_abv(self):
        total_volume = 1
        total_alcohol = 0

        for ingredient in self.recipe.all():
            if ingredient.get_unit_display() in ['ml', 'parts']:
                total_alcohol += ingredient.volume*ingredient.ingredient.abv 
                total_volume += ingredient.volume

        return round(total_alcohol/total_volume, 1)

    def __str__(self):
        return self.name