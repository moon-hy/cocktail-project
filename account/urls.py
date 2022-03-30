from django.urls import path

from account.views import *


urlpatterns = [
    path('account', AccountView.as_view(), name='account'),
]
