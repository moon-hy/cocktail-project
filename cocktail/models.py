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
    ('any', 'any',),
    ('hot-drink', 'hot-drink'),
    ('collins', 'collins'),
    ('highball', 'highball'),
    ('martini', 'martini'),
    ('hurricane', 'hurricane'),
    ('white-wine', 'white-wine'),
    ('old-fashoined', 'old-fashioned'),
    ('margarita', 'margarita'),
    ('shot', 'shot'),
    ('champagne-tulip', 'champagne-tulip'),
    ('champagne-flute', 'champagne-flute'),
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
    name        = models.CharField(max_length=255)
    base        = models.CharField(max_length=32, choices=COCKTAIL_BASE)
    glass       = models.CharField(max_length=32, choices=COCKTAIL_GLASS, default='any')
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

    def is_available(self, account):
        return all([ingredient in account.shelf for ingredient in self.ingredients])
