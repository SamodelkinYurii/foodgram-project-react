import django_filters as filters

from ingredients.models import Ingredient
from recipes.models import Recipe
from tags.models import Tag


class IngredientSearchFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name="name",
        lookup_expr="istartswith",
    )

    class Meta:
        model = Ingredient
        fields = []


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name="tags__slug",
        to_field_name="slug",
    )

    class Meta:
        model = Recipe
        fields = (
            "author",
            "tags",
        )
