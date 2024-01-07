from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Recipe
from .serializers import RecipeSerializer




class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post"]
    pagination_class = PageNumberPagination
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
