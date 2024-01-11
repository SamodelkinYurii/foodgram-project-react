import django_filters as filters

from tags.models import Tag

from .models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name="tags__slug",
        to_field_name="slug",
    )
    is_favorited = filters.CharFilter(field_name='is_favorited')
    is_in_shopping_cart = filters.CharFilter(field_name='is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ("author", "tags", )
