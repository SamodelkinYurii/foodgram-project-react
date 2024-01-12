import django_filters as filters

from tags.models import Tag

from .models import Recipe


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
