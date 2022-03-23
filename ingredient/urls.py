from django.urls import path

from ingredient.views import *


urlpatterns = [
    path('categories', CategoryList.as_view(), name='category_list'),
    path('ingredients', IngredientList.as_view(), name='ingredient_list'),
    path('ingredients/<int:pk>', IngredientDetail.as_view(), name='ingredient_detail'),
    path('ingredients/category/<int:pk>', IngredientCategoryList.as_view(), name='ingredient_category_list'),
]
