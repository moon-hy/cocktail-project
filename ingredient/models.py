from django.db import models

# Create your models here.
class Base(models.Model):
    name        = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    abv         = models.DecimalField(max_digits=3, decimal_places=1, default=0)

class Category(models.Model):
    name        = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Ingredient(Base):
    category    = models.ForeignKey(
        'Category',
        related_name='ingredients',
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.name
