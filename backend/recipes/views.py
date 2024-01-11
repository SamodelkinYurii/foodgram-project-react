from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import FavoriteRecipe, Recipe, ShoppingcartRecipe
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    FavoriteRecipeSerializer,
    ModRecipeSerializer,
    ReadRecipeSerializer,
    ShoppingcartRecipeSerializer,
)


class RecipeViewSet(viewsets.ModelViewSet):
    # http_method_names = ["get", "post"]
    pagination_class = LimitOffsetPagination
    queryset = Recipe.objects.all()
    # serializer_class = ReadRecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadRecipeSerializer
        return ModRecipeSerializer

    @action(
        detail=True,
        methods=("POST",),
        permission_classes=[permissions.IsAuthenticated],
        # permission_classes=[IsAuthorOrReadOnly],
    )
    def favorite(self, request, pk):
        current_user = self.request.user
        serializer = FavoriteRecipeSerializer(
            data={"recipe": pk, "favorite": current_user.id},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        current_user = self.request.user
        check_favorite = FavoriteRecipe.objects.filter(
            recipe=pk, favorite=current_user.id
        )
        if check_favorite.exists():
            check_favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=("POST",),
        # permission_classes=[IsAuthorOrReadOnly],
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        current_user = self.request.user
        serializer = ShoppingcartRecipeSerializer(
            data={"recipe": pk, "shoppingcart": current_user.id},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        current_user = self.request.user
        check_favorite = ShoppingcartRecipe.objects.filter(
            recipe=pk, shoppingcart=current_user.id
        )
        if check_favorite.exists():
            check_favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
