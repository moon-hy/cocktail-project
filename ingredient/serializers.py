from pyexpat import model
from rest_framework import serializers

from ingredient.models import Category, Ingredient


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model   = Category
        fields  = [
            'id', 'name',
        ]
        
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Ingredient
        fields  = [
            'id', 'name', 'description', 'abv', 'category', 'cocktails',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = instance.category.name

        return representation
