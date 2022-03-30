from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)

from django.contrib.auth.models import User

from authentication.serializers import SignupSerializer, UserListSerializer


class UserView(APIView):
    def get_authenticators(self):
        authentication_classes = ()

        if self.request.method != 'POST':
            authentication_classes = (TokenAuthentication,)
        
        return [authentication() for authentication in authentication_classes]

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = (IsAdminUser, )
        elif self.request.method == 'POST':
            permission_classes = (AllowAny, )
        else:
            permission_classes = (IsAuthenticated, )

        return [permission() for permission in permission_classes]

    def get(self, request):
        print( request.user, request.user.account)
        users       = User.objects.all()
        serializer  = UserListSerializer(users, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        user        = request.data.get('user', {})
        serializer  = SignupSerializer(data=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
