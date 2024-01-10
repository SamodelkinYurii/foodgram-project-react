from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

# from rest_framework import filters
from .filters import IngredientSearchFilter
from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # filter_backends = [DjangoFilterBackend]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter
