from rest_framework import serializers

from django.db import transaction

from cocktail.models import Cocktail, Method, Recipe, Tag


class MethodSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Method
        fields  = [
            'name',
        ]
    
    def to_representation(self, instance):
        return {
            'id'    : instance.id,
            'name'  : instance.name,
        }

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Recipe
        fields  = '__all__'

    def to_representation(self, instance):
        representation = {
            'id'            : instance.ingredient.id,
            'name'          : instance.ingredient.name,
            'volume'        : instance.volume,
            'unit'          : instance.unit
        }
        if instance.optional:
            representation['optional'] = True
            
        return representation

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Tag
        fields  = [
            'name',
        ]
    
    def to_representation(self, instance):
        return {
            'name'  : instance.name,
        }

class CocktailSerializer(serializers.ModelSerializer):
    ingredients = RecipeSerializer(
        source='recipe',
        many=True
    )
    
    class Meta:
        model   = Cocktail
        fields  = [
            'id', 'name', 'base', 'garnish', 'methods', 'description', 'ingredients', 'tags', 'abv',
        ]
    
    def create(self, validated_data):
        with transaction.atomic():
            ingredients     = validated_data.pop('recipe', [])
            methods         = validated_data.pop('methods', [])
            tags            = validated_data.pop('tags',[])

            cocktail = Cocktail.objects.create(**validated_data)
            for ingredient in ingredients:
                """ Create Middle Table """
                Recipe.objects.create(
                    cocktail=cocktail, **ingredient,
                ).save()

            for tag in tags:
                cocktail.tags.add(tag)

            for method in methods:
                cocktail.methods.add(method)

            cocktail.save()
            return cocktail
