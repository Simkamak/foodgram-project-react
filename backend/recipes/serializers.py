from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Tag, Ingredient, Recipe, IngredientForRecipe, Follow, Favorites, Purchase
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'author', 'user']


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data["user"]
        recipe = validated_data["recipe"]
        obj, created = Favorites.objects.get_or_create(user=user, recipe=recipe)
        if not created:
            raise serializers.ValidationError(
                {
                    "message": "Нельзя добавить повторно в избранное"
                }
            )
        return validated_data


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data["user"]
        recipe = validated_data["recipe"]
        obj, created = Purchase.objects.get_or_create(user=user, recipe=recipe)
        if not created:
            raise serializers.ValidationError(
                {"message": "Вы уже добавили рецепт в корзину"}
            )
        return validated_data


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField()

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientForRecipe
        fields = ['id', 'name', 'amount', 'measurement_unit']


class IngredientForRecipeCreate(serializers.Serializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientForRecipeCreate(many=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'text',
            'cooking_time', 'pub_date'
        ]

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorites.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Purchase.objects.filter(user=request.user, recipe=obj).exists()

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        for ingredient_data in ingredients_data:
            ingredient_instance = get_object_or_404(Ingredient, pk=ingredient_data['id'])
            IngredientForRecipe.objects.create(
                ingredient=ingredient_instance,
                recipe=recipe,
                amount=ingredient_data.get('amount')
            )
        return recipe


class RecipeReadSerializer(RecipeSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        ingredients = IngredientForRecipe.objects.filter(recipe=obj)
        return IngredientForRecipeSerializer(ingredients, many=True).data



