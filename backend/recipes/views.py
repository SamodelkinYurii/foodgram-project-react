from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import serializers

from .models import Recipe
from .serializers import ModRecipeSerializer, ReadRecipeSerializer, FavoriteRecipeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class RecipeViewSet(viewsets.ModelViewSet):
    # http_method_names = ["get", "post"]
    pagination_class = LimitOffsetPagination
    queryset = Recipe.objects.all()
    # serializer_class = ReadRecipeSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadRecipeSerializer
        return ModRecipeSerializer

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        # permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request):
        serializer = FavoriteRecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"recipe": serializer.data})

