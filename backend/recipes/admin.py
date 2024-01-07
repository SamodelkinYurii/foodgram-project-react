from django.contrib import admin
from django import forms

from .models import Recipe
from tags.models import Tag
from ingredients.models import Ingredient


# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):

#     list_display = ("author", "image", "name", "text", "cooking_time",'get_tags')
#     ordering = ('id',) 

#     @admin.display(description='tags')
#     def get_tags(self, obj):
#         return [tag.name for tag in obj.tag_set.all()]

@admin.register(Recipe)
class ProductAdmin(admin.ModelAdmin):      # Here  
    # list_display = ('id', 'name', 'price', 'get_categories')
    list_display = ('get_tags', "author", 'get_ingredients', "name", "image", "text", "cooking_time",)
    ordering = ('id',)
    

    @admin.display(description='tags')
    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]
    
    @admin.display(description='ingredients')
    def get_ingredients(self, obj):
        return [ingredient.name for ingredient in obj.ingredients.all()]
