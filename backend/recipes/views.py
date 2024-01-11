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
    pagination_class = LimitOffsetPagination
    queryset = Recipe.objects.all()
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
    )
    def favorite(self, request, pk):
        current_user = self.request.user
        check_favorite = FavoriteRecipe.objects.filter(recipe=pk, favorite=current_user)
        if check_favorite.exists():
            return Response(
                {"detail": "Вы уже добавили рецепт в избранное"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = FavoriteRecipeSerializer(
            data={"recipe": pk, "favorite": current_user.id},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        check_recipe = Recipe.objects.filter(id=pk)
        current_user = self.request.user
        check_favorite = FavoriteRecipe.objects.filter(
            recipe=pk, favorite=current_user.id
        )
        if not check_recipe.exists():
            return Response(
                {"detail": "Нельзя убрать из избранного несуществующий рецепт"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if check_favorite.exists():
            check_favorite.delete()
            return Response({"detail": "Рецепт удален из избранного"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Рецепта нет в избранном"}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=("POST",),
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        current_user = self.request.user
        check_shopping_car = ShoppingcartRecipe.objects.filter(recipe=pk, shoppingcart=current_user)
        if check_shopping_car.exists():
            return Response(
                {"detail": "Вы уже добавили рецепт в корзину"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = ShoppingcartRecipeSerializer(
            data={"recipe": pk, "shoppingcart": current_user.id},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        check_recipe = Recipe.objects.filter(id=pk)
        current_user = self.request.user
        check_favorite = ShoppingcartRecipe.objects.filter(
            recipe=pk, shoppingcart=current_user.id
        )
        if not check_recipe.exists():
            return Response(
                {"detail": "Нельзя убрать из корзины несуществующий рецепт"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if check_favorite.exists():
            check_favorite.delete()
            return Response({"detail": "Рецепт удален из корзины"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Рецепта нет в корзине"}, status=status.HTTP_400_BAD_REQUEST)
