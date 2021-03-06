from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from django.http import Http404

from ingredient.models import Category, Ingredient
from ingredient.serializers import CategorySerializer, IngredientSerializer


class CategoryList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        category    = Category.objects.all()
        serializer  = CategorySerializer(category, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class IngredientList(APIView):
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = (IsAuthenticated, )
        else:
            permission_classes = (IsAdminUser, )
        return [permission() for permission in permission_classes]

    def get(self, request):
        ingredients = Ingredient.objects.all()

        if query := request.query_params.get('query'):
            ingredients = ingredients.filter(name__icontains=query)
            
        if category := request.query_params.get('category'):
            ingredients = ingredients.filter(category=category)

        serializer  = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer  = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class IngredientDetail(APIView):
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = (IsAuthenticated, )
        else:
            permission_classes = (IsAdminUser, )
        return [permission() for permission in permission_classes]

    def get_object(self, pk):
        try:
            return Ingredient.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        ingredient  = self.get_object(pk)
        serializer  = IngredientSerializer(ingredient)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        ingredient  = self.get_object(pk)
        serializer  = IngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        ingredient  = self.get_object(pk)
        serializer  = IngredientSerializer(ingredient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        ingredient  = self.get_object(pk)
        ingredient.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class IngredientCategoryList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        ingredients = Ingredient.objects.filter(category=pk)
        serializer  = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class IngredientShelve(APIView):
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = (IsAuthenticated, )
        else:
            permission_classes = (IsAdminUser, )
        return [permission() for permission in permission_classes]
        
    def get(self, request, pk):
        account     = request.user.account
        ingredient  = Ingredient.objects.get(pk=pk)
        
        return Response({
            'ingredient': ingredient.name,
            'shelved': account.is_shelved(ingredient),
        })

    def post(self, request, pk):
        account     = request.user.account
        ingredient  = Ingredient.objects.get(pk=pk)
        account.shelve(ingredient)

        serializer  = IngredientSerializer(ingredient)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete(self, request, pk):
        account     = request.user.account
        ingredient  = Ingredient.objects.get(pk=pk)
        account.unshelve(ingredient)

        return Response(status=HTTP_204_NO_CONTENT)
