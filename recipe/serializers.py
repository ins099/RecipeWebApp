from  rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id','author', 'title', 'description', 'category', 'ingredients', 'procedure', 'img']
         