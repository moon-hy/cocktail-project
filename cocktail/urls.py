from django.urls import path

from cocktail.views import *


urlpatterns = [
    path('cocktails', CocktailList.as_view(), name='cocktail_list'),
    path('cocktails/<int:pk>', CocktailDetail.as_view(), name='cocktail_detail'),
    path('cocktails/tags', CocktailTag.as_view(), name='cocktail_tag_list'),
    path('cocktails/tags/<str:pk>', CocktailListByTag.as_view(), name='cocktail_list_tag'),
    path('cocktails/favorites/<int:pk>', CocktailFavorite.as_view(), name='cocktail_fav'),
    path('cocktails/available', CocktailAvilable.as_view(), name='cocktail_available'),
]
