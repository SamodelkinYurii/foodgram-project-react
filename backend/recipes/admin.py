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
        "favorite",
    )


@admin.register(ShoppingcartRecipe)
class ShoppingcartRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "recipe",
        "shoppingcart",
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
    )
    ordering = ("id",)
    inlines = (IngredientRecipetInline,)

    @admin.display(description="tags")
    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    # @admin.display(description='Ингредиенты')
    # def ingredients(self, obj):
    #     return list(obj.ingredients.values_list('name', flat=True))
    # @admin.display(description='ingredients')
    # def get_ingredients(self, obj):
    #     return [ingredient.name for ingredient in obj.ingredients.all()]
