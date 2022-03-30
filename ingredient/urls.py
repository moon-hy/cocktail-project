from django.urls import path

from ingredient.views import *


urlpatterns = [
    path('ingredients', IngredientList.as_view(), name='ingredient_list'),
    path('ingredients/<int:pk>', IngredientDetail.as_view(), name='ingredient_detail'),
    path('ingredients/<int:pk>/shelve', IngredientShelve.as_view(), name='ingredient_shelf'),
]
