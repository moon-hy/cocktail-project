from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK
)

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q, Count

from account.models import Account
from account.serializers import AccountSerializer
from cocktail.models import Cocktail


class AccountListView(APIView):
    def get(self, request):
        users       = Account.objects.all()
        serializer  = AccountSerializer(users, many=True)
        
        return Response(serializer.data, status=HTTP_200_OK)

class AccountView(APIView):
    def get(self, request):
        account     = request.user.account
        serializer  = AccountSerializer(account)

        return Response(serializer.data, status=HTTP_200_OK)
