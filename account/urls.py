from django.urls import path

from account.views import *


urlpatterns = [
    #path('accounts', AccountListView.as_view()),
    path('account', AccountView.as_view(), name='account'),
]
