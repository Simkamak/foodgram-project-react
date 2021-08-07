from rest_framework import filters, permissions, status, viewsets
from .serializers import TagSerializer, RecipeReadSerializer, RecipeSerializer, CustomUserSerializer, IngredientSerializer, \
    ShowFollowsSerializer, FollowSerializer
from .models import Tag, Recipe, IngredientForRecipe, Ingredient, Purchase, Favorites, Follow
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from .filters import IngredientNameFilter
import django_filters.rest_framework
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

User = get_user_model()


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filter_class = RecipeFilter
    pagination_class = PageNumberPagination


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


#class UsersViewSet(viewsets.ReadOnlyModelViewSet):
#    serializer_class = CustomUserSerializer
#    queryset = User.objects.all()
#    permission_classes = AllowAny
#    pagination_class = PageNumberPagination


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def show_follows(request):
    user_obj = User.objects.filter(following__user=request.user)
    paginator = PageNumberPagination()
    paginator.page_size = 6
    result_page = paginator.paginate_queryset(user_obj, request)
    serializer = ShowFollowsSerializer(
        result_page, many=True, context={'current_user': request.user})
    return paginator.get_paginated_response(serializer.data)


class FollowView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'delete']

    def get(self, request, user_id):
        user = request.user
        author = get_object_or_404(User, id=user_id)
        serializer = FollowSerializer(
            data={'user': user.id, 'author': user_id}
        )
        if request.method == "GET":
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            #return Response(f'{user} подписался от {author}', status=status.HTTP_201_CREATED)
            #follow = get_object_or_404(Follow, user=user, author=author)
            serializer = ShowFollowsSerializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        user = request.user
        author = get_object_or_404(User, id=user_id)
        follow = get_object_or_404(Follow, user=user, author=author)
        follow.delete()
        return Response(f'{user} отписался от {author}', status=status.HTTP_204_NO_CONTENT)

