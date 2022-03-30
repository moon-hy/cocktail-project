from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ingredient.urls')),
    path('api/', include('cocktail.urls')),
    path('api/', include('account.urls')),
]
