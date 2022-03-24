from django.urls import path

from cocktail.views import *


urlpatterns = [
    path('cocktails', CocktailList.as_view(), name='cocktail_list'),
    path('cocktails/<int:pk>', CocktailDetail.as_view(), name='cocktail_detail'),
    path('cocktails/base', CocktailBase.as_view(), name='cocktail_base_list'),
    path('cocktails/base/<int:pk>', CocktailListByBase.as_view(), name='cocktail_list_base'),
    path('cocktails/tag', CocktailTag.as_view(), name='cocktail_tag_list'),
    path('cocktails/tag/<int:pk>', CocktailListByTag.as_view(), name='cocktail_list_tag')
]
