from rest_framework.views import APIView
from rest_framework.response import Response
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
    def get(self, request):
        category    = Category.objects.all()
        serializer  = CategorySerializer(category, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class IngredientList(APIView):
    def get(self, request):
        ingredients = Ingredient.objects.all()
        serializer  = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer  = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class IngredientDetail(APIView):
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
    def get(self, request, pk):
        ingredients = Ingredient.objects.filter(category=pk)
        serializer  = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
