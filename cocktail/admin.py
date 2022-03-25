from django.contrib import admin

from cocktail.models import (
    Cocktail, Tag, Recipe, Method
)
# Register your models here.
class RecipeInline(admin.TabularInline):
    model = Recipe
    extra = 3

class CocktailAdmin(admin.ModelAdmin):
    readonly_fields = ('abv',)
    inlines = (RecipeInline,)

admin.site.register(Cocktail, CocktailAdmin)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Method)
