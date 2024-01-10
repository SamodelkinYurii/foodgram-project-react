import django_filters as filters

from .models import Ingredient


class IngredientSearchFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name="name",
        lookup_expr="istartswith",
    )

    class Meta:
        model = Ingredient
        fields = []
