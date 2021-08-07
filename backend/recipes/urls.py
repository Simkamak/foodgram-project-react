from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagsViewSet, RecipesViewSet, IngredientViewSet, show_follows, FollowView

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('users/subscriptions/', show_follows, name='subscriptions'),
    path('users/<int:user_id>/subscribe/', FollowView.as_view(), name='subscribe'),
    path('', include(router.urls)),

]