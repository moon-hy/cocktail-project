from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'Category',
        related_name='subs',
        on_delete=models.CASCADE
    )

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    abv = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    category = models.ForeignKey(
        'SubCategory',
        related_name='ingredients',
        on_delete=models.CASCADE
    )
