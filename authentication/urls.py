from django.urls import path

from authentication.views import *


urlpatterns = [
    path('users', UserView.as_view(), name='auth_users'),
]
