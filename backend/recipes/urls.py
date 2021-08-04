from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagsViewSet, RecipesViewSet, IngredientViewSet, UsersViewSet

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [path('', include(router.urls))]