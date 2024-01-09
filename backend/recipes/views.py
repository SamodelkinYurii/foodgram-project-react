from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Recipe
from .serializers import ModRecipeSerializer, ReadRecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    # http_method_names = ["get", "post"]
    pagination_class = PageNumberPagination
    queryset = Recipe.objects.all()
    serializer_class = ReadRecipeSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadRecipeSerializer
        return ModRecipeSerializer
