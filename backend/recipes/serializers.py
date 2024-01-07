from rest_framework import serializers
# from django.core import serializers

from .models import Recipe, IngredientRecipe
from ingredients.models import Ingredient
from tags.serializers import TagSerializer
from users.serializers import UserSerializer
from ingredients.serializers import IngredientSerializer

class IngredientRecipeSerializer(serializers.ModelSerializer):
    

    id = serializers.PrimaryKeyRelatedField(
        source='ingredients.id', queryset=Ingredient.objects.all()
    )
    measurement_unit = serializers.CharField(
        source='ingredients.measurement_unit', read_only=True
    )
    name = serializers.CharField(source='ingredients.name', read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )

# class RecipeRetriveSerializer(serializers.ModelSerializer):
#     """ Сериализатор для чтения рецептов. """

#     image = Base64ImageField()
#     tags = TagSerializer(many=True)
#     author = UserSerializer(read_only=True,
#                             default=serializers.CurrentUserDefault())
#     ingredients = IngredientRetriveSerializer(many=True,
#                                               source='ingredientrecipe')
#     is_favorited = serializers.BooleanField(read_only=True, default=0)
#     is_in_shopping_cart = serializers.BooleanField(read_only=True, default=0)

#     class Meta:
#         model = Recipe
#         exclude = ('pub_date',)

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    # ingredients = IngredientRecipeSerializer(many=True, source='ingredientrecipe')
    ingredients = serializers.SerializerMethodField()
    # ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            # "is_favorited",
            # "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        
    def get_ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe_id=obj.id)
        return IngredientRecipeSerializer(ingredients, many=True).data
    # def get_ingredients(self, obj):
    #     qs = IngredientRecipe.objects.all()
    #     qs_json = serializers.serialize('json', qs)

    #     return qs_json
        # ingredients = IngredientRecipe.objects.all()
        # recipe = obj.id
        # qs = IngredientRecipe.objects.all()
        # qs_json = serializers.serialize('json', qs)
        # # print(obj.ingredientrecipe.filter(recipe=obj.id))
        # return qs_json
        # return obj.ingredientrecipe.filter(recipe=obj.id)
        # user = self.context.get("request").user
    #     return all(
    #         (
    #             (not user.is_anonymous),
    #             obj.subscriber.filter(
    #                 user=user.id, subscriber=obj.id
    #             ).exists(),
    #         )
    #     )
