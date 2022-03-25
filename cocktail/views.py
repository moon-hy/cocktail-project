from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from django.http import Http404

from cocktail.models import Cocktail, Tag
from cocktail.serializers import CocktailSerializer, CocktailListSerializer, TagSerializer


def cocktail_filter(cocktails, request):
    if query := request.query_params.get('query'):
        cocktails = cocktails.filter(name__icontains=query)

    if base := request.query_params.get('base'):
        cocktails = cocktails.filter(base=base)

    if min_abv := request.query_params.get('min'):
        cocktails = cocktails.filter(abv__gte=min_abv)

    if max_abv := request.query_params.get('max'):
        cocktails = cocktails.filter(abv__lte=max_abv)

    return cocktails

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
        cocktails   = cocktail_filter(cocktails, request)
        serializer  = CocktailListSerializer(cocktails, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class CocktailList(APIView):
    def get(self, request):
        cocktails   = Cocktail.objects.all()
        cocktails   = cocktail_filter(cocktails, request)
        serializer  = CocktailListSerializer(cocktails, many=True)
        meta        = {
            'total_count': cocktails.count()
        }
        return Response({
            'meta': meta,
            'cocktails': serializer.data
        }, status=HTTP_200_OK)
    
    def post(self, request):
        """태그가 없으면 추가."""
        if tags := request.data.get('tags'):
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(pk=tag)
                if created:
                    tag_obj.save()
        
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
