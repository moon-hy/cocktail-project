from re import search
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from django.http import Http404

from cocktail.models import Base, Cocktail, Tag
from cocktail.serializers import CocktailSerializer, BaseSerializer, TagSerializer

class CocktailBase(APIView):
    def get(self, request):
        bases       = Base.objects.all()
        serializer  = BaseSerializer(bases, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class CocktailListByBase(APIView):
    def get(self, request, pk):
        base        = Base.objects.get(pk=pk)
        cocktails   = base.cocktails
        serializer  = CocktailSerializer(cocktails, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class CocktailTag(APIView):
    def get(self, request):
        query      = request.query_params.get('query')
        tags        = Tag.objects.all()
        if query:
            tags    = tags.filter(name__icontains=query)
        serializer  = TagSerializer(tags, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class CocktailListByTag(APIView):
    def get(self, request, pk):
        tag         = Tag.objects.get(pk=pk)
        cocktails   = tag.cocktails
        serializer  = CocktailSerializer(cocktails, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class CocktailList(APIView):
    def get(self, request):
        """
        GET /cocktails?query={query}
        """
        query       = request.query_params.get('query')
        cocktails   = Cocktail.objects.all()
        if query:
            cocktails = cocktails.filter(name__icontains=query)
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

    def delete(self, request, pk):
        cocktail    = self.get_object(pk)
        cocktail.delete()
        return Response(status=HTTP_204_NO_CONTENT)
