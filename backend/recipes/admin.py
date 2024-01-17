from django.contrib import admin

from .models import (
    FavoriteRecipe,
    IngredientRecipe,
    Recipe,
    ShoppingcartRecipe,
)


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "recipe",
        "user",
    )


@admin.register(ShoppingcartRecipe)
class ShoppingcartRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "recipe",
        "user",
    )


class IngredientRecipetInline(admin.TabularInline):
    model = IngredientRecipe
    min_num = 1


@admin.register(Recipe)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "get_tags",
        "author",
        "name",
        "image",
        "text",
        "cooking_time",
        "favorite",
    )
    ordering = ("id",)
    list_filter = ["name", "author", "tags"]
    inlines = (IngredientRecipetInline,)

    @admin.display(description="tags")
    def get_tags(self, obj):
        return ", ".join(list(obj.tags.values_list("name", flat=True)))

    @admin.display(description="Рецепт в избранном")
    def favorite(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj.id).count()
