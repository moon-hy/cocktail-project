from django.contrib import admin

from ingredient.models import (
    Ingredient, Category
)
# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Category)
