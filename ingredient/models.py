from django.db import models

# Create your models here.
class Base(models.Model):
    name        = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    abv         = models.DecimalField(max_digits=3, decimal_places=1, default=0)

class Category(models.Model):
    name        = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.name

class Ingredient(Base):
    category    = models.ForeignKey(
        'Category',
        related_name='ingredients',
        on_delete=models.CASCADE
    )
    
    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.category}|{self.name}|{self.abv}'
