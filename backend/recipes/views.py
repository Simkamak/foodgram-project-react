from rest_framework import filters, permissions, status, viewsets
from .serializers import TagSerializer, RecipeReadSerializer, RecipeSerializer, CustomUserSerializer, IngredientSerializer,IngredientForRecipeSerializer
from .models import Tag, Recipe, IngredientForRecipe, Ingredient, Purchase, Favorites, Follow
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from .filters import IngredientNameFilter
import django_filters.rest_framework
from django.contrib.auth import get_user_model
User = get_user_model()


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    #queryset = Recipe.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filter_class = RecipeFilter
    pagination_class = PageNumberPagination
    #serializer_class = RecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_in_shopping_cart = self.request.query_params.get(
            "is_in_shopping_cart"
        )
        is_favorited = self.request.query_params.get("is_favorited")
        cart = Purchase.objects.filter(user=self.request.user.id)
        favorite = Favorites.objects.filter(user=self.request.user.id)

        if is_in_shopping_cart == "true":
            queryset = queryset.filter(cart__in=cart)
        elif is_in_shopping_cart == "false":
            queryset = queryset.exclude(cart__in=cart)
        if is_favorited == "true":
            queryset = queryset.filter(favorite__in=favorite)
        elif is_favorited == "false":
            queryset = queryset.exclude(favorite__in=favorite)
        return queryset.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return RecipeReadSerializer
        return RecipeSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny, )
    pagination_class = None
    filterset_class = IngredientNameFilter


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    permission_classes = AllowAny
    pagination_class = PageNumberPagination

