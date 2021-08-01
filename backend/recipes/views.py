from rest_framework import filters, permissions, status, viewsets
from .serializers import TagSerializer, RecipeSerializer, IngredientSerializer, IngredientForRecipeSerializer
from .models import Tag, Recipe, IngredientForRecipe, Ingredient
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
import django_filters.rest_framework


class TagsViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    #filter_class = RecipeFilter
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]

