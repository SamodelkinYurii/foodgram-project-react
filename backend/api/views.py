import io
import os

from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.filters import IngredientSearchFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    FavoriteRecipeSerializer,
    IngredientSerializer,
    ModRecipeSerializer,
    ReadRecipeSerializer,
    ShoppingcartRecipeSerializer,
    SubscribeSerializer,
    SubscriptionSerializer,
    TagSerializer,
    UserSerializer,
)
from api.utils import AddDelMixin
from ingredients.models import Ingredient
from recipes.models import (
    FavoriteRecipe,
    IngredientRecipe,
    Recipe,
    ShoppingcartRecipe,
)
from tags.models import Tag
from users.models import Subscribe, User


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter


class UserViewSet(UserViewSet):
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "me":
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    @action(
        detail=True,
        methods=("POST",),
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, id):
        check_user = User.objects.filter(id=id)
        if not check_user.exists():
            return Response(
                {"detail": "Нельзя подписатся на несуществующего автора"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = SubscribeSerializer(
            data={"user": self.request.user.id, "subscriber": id},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        check_user = User.objects.filter(id=id)
        current_user = self.request.user
        check_subscribe = Subscribe.objects.filter(
            user=current_user, subscriber=id
        )
        if not check_user.exists():
            return Response(
                {"detail": "Нельзя отписатся от несуществующего автора"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if check_subscribe.exists():
            check_subscribe.delete()
            return Response(
                {"detail": "Вы отписались от автора"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"detail": "Вы уже отписаны от автора"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=False,
        methods=("GET",),
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscriptions(self, request):
        current_user = self.request.user
        queryset = User.objects.filter(subscriber__user=current_user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(AddDelMixin, viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        is_favorited_param = self.request.query_params.get(
            "is_favorited", None
        )
        is_in_shopping_cart = self.request.query_params.get(
            "is_in_shopping_cart", None
        )
        current_user = self.request.user
        if all(
            (is_favorited_param == "1", self.request.user.is_authenticated)
        ):
            return Recipe.objects.filter(favorite__user=current_user.id)
        elif all(
            (is_in_shopping_cart == "1", self.request.user.is_authenticated)
        ):
            return Recipe.objects.filter(shopping_cart__user=current_user.id)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadRecipeSerializer
        return ModRecipeSerializer

    @action(
        detail=True,
        methods=("POST", "DELETE"),
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk):
        if request.method == "POST":
            return self.create_entry(FavoriteRecipeSerializer, request, pk)
        return self.delete_entry(FavoriteRecipe, request, pk, "favorite")

    @action(
        detail=True,
        methods=("POST", "DELETE"),
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        if request.method == "POST":
            return self.create_entry(ShoppingcartRecipeSerializer, request, pk)
        return self.delete_entry(
            ShoppingcartRecipe, request, pk, "shopping_cart"
        )

    def save_pdf(self, ingredients, current_user):
        buffer = io.BytesIO()
        fonts = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "font_files/",
            "ArialRegular.ttf",
        )
        pdfmetrics.registerFont(ttfonts.TTFont("ArialRegular", fonts))
        pdf = canvas.Canvas(buffer)
        pdf.saveState()
        pdf.setFont("ArialRegular", 24)
        pdf.drawString(100, 742, "СПИСОК ПОКУПОК:")
        pdf.setFont("ArialRegular", 14)
        line = 712
        n = 1
        for ingredient in ingredients:
            pdf.drawString(
                100,
                line,
                f"{n}. {ingredient['ingredient__name']} - "
                f"{ingredient['sum_amount']} "
                f"{ingredient['ingredient__measurement_unit']}",
            )
            line -= 20
            n += 1
        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        return buffer

    @action(
        detail=False,
        methods=("GET",),
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        current_user = request.user
        ingredients_in_shopping_cart = Recipe.objects.filter(
            shopping_cart__user=current_user
        ).values_list("id", flat=True)
        if not ingredients_in_shopping_cart.exists():
            return Response(
                {"detail": "Конзина с рецептами пуста"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ingredients = (
            IngredientRecipe.objects.filter(
                recipe__in=ingredients_in_shopping_cart
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(sum_amount=Sum("amount"))
        )

        return FileResponse(
            self.save_pdf(ingredients, current_user),
            as_attachment=True,
            filename=f"{current_user.username}_shop_cart.pdf",
            status=status.HTTP_200_OK,
        )
