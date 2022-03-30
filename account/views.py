from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK
)

from account.serializers import AccountSerializer


class AccountView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        account     = request.user.account
        serializer  = AccountSerializer(account)

        return Response(serializer.data, status=HTTP_200_OK)
