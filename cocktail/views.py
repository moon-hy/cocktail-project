from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from django.http import Http404
from django.db.models import Q, Count

from cocktail.models import Cocktail, Tag
from cocktail.serializers import CocktailSerializer, CocktailListSerializer, TagSerializer
from config.permissions import IsOwnerOnly


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
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        query      = request.query_params.get('query')
        tags        = Tag.objects.all()
        if query:
            tags    = tags.filter(name__icontains=query)
        serializer  = TagSerializer(tags, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class CocktailListByTag(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        tag         = Tag.objects.get(pk=pk)
        cocktails   = tag.cocktails
        cocktails   = cocktail_filter(cocktails, request)
        serializer  = CocktailListSerializer(cocktails, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class CocktailList(APIView):
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = (IsAuthenticated, )
        else:
            permission_classes = (IsAdminUser, )
        return [permission() for permission in permission_classes]
        
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
        """????????? ????????? ??????."""
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
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = (IsAuthenticated, )
        else:
            permission_classes = (IsAdminUser, )
        return [permission() for permission in permission_classes]
        
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

class CocktailFavorite(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsOwnerOnly, IsAuthenticated)

    def get(self, request, pk):
        account     = request.user.account
        cocktail    = Cocktail.objects.get(pk=pk)

        return Response({
            'favorited': account.is_favorited(cocktail),
            'total_number': cocktail.favorited.count()
        })

    def post(self, request, pk):
        account     = request.user.account
        cocktail    = Cocktail.objects.get(pk=pk)
        account.favorite(cocktail)

        serializer  = CocktailSerializer(cocktail)

        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete(self, request, pk):
        account     = request.user.account
        cocktail    = Cocktail.objects.get(pk=pk)
        account.unfavorite(cocktail)

        return Response(status=HTTP_204_NO_CONTENT)

class CocktailAvilable(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsOwnerOnly, IsAuthenticated)
    
    def get(self, request):
        account     = request.user.account
        shelf_set   = set(account.shelf.all())
        q           = Q(recipe__ingredient__in=shelf_set) | Q(recipe__optional=True)

        cocktails   = Cocktail.objects.annotate(
                matches=Count('recipe', filter=q)
            ).filter(
                matches__gte=Count('recipe')
            ).prefetch_related(
                'ingredients'
            )

        serializer  = CocktailListSerializer(cocktails, many=True)

        meta        = {
            'total_count': cocktails.count()
        }
        
        return Response({
            'meta': meta,
            'cocktails': serializer.data
        }, status=HTTP_200_OK)
