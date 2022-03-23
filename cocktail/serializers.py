from ctypes.wintypes import tagSIZE
from rest_framework import serializers

from cocktail.models import Cocktail, Recipe, Tag


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Recipe
        fields  = '__all__'

    def to_representation(self, instance):
        representation = {
            'id'            : instance.ingredient.id,
            'ingredient'    : instance.ingredient.name,
            'volume'        : instance.volume,
            'unit'          : instance.get_unit_display()
        }
        return representation

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Tag
        fields  = [
            'name',
        ]

    def to_representation(self, instance):
        representation = {
            'id'            : instance.id,
            'name'          : instance.name
        }
        return representation

class CocktailSerializer(serializers.ModelSerializer):
    ingredients = RecipeSerializer(source='recipe', many=True)
    abv         = serializers.SerializerMethodField(method_name='get_abv', read_only=True)
    tags        = TagSerializer(many=True)

    class Meta:
        model   = Cocktail
        fields  = [
            'id', 'name', 'base', 'garnish', 'description', 'ingredients', 'tags', 'abv',
        ]
    
    def create(self, validated_data):
        ingredients     = validated_data.pop('recipe', [])
        tags            = validated_data.pop('tags',[])

        cocktail = Cocktail.objects.create(**validated_data)
        for ingredient in ingredients:
            """ Create Middle Table """
            Recipe.objects.create(
                cocktail=cocktail, **ingredient,
            ).save()

        for tag in tags:
            """ Add ManyToMany Tag """
            cocktail.tags.add(tag)

        return cocktail

    def to_representation(self, instance):
        representation  = super().to_representation(instance)
        representation['base']  = instance.get_base_display()
        return representation

    def get_abv(self, instance):
        total_volume = 1
        total_alcohol = 0

        for ingredient in instance.recipe.all():
            total_alcohol += ingredient.volume*ingredient.ingredient.abv 
            total_volume += ingredient.volume

        return round(total_alcohol/total_volume, 1)
