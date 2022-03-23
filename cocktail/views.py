from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from django.http import Http404

from cocktail.models import Cocktail
from cocktail.serializers import CocktailSerializer


class CocktailList(APIView):
    def get(self, request):
        cocktails   = Cocktail.objects.all()
        serializer  = CocktailSerializer(cocktails, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request):
        serializer  = CocktailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class CocktailDetail(APIView):
    def get_object(self, pk):
        try:
            return Cocktail.objects.get(pk=pk)
        except:
            raise Http404
    
    def get(self, request, pk):
        cocktail    = self.get_object(pk)
        serializer  = CocktailSerializer(cocktail)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        cocktail    = self.get_object(pk)
        serializer  = CocktailSerializer(cocktail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.data, status=HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        cocktail    = self.get_object(pk)
        serializer  = CocktailSerializer(cocktail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.data, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cocktail    = self.get_object(pk)
        cocktail.delete()
        return Response(status=HTTP_204_NO_CONTENT)
