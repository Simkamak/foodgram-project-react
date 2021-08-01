from rest_framework import serializers
from users.serializers import CustomUserSerializer
from .models import Tag, Ingredient, Recipe, IngredientForRecipe, Follow
from user.models import CustomUser


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ['id', 'author', 'user']


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientForRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientForRecipe
        fields = ['id', 'recipe', 'ingredient', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    author = CustomUserSerializer
    ingredient = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = []

