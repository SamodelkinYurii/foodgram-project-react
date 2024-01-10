from django.shortcuts import get_object_or_404
from rest_framework import serializers

from ingredients.models import Ingredient
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserSerializer
from users.models import User

from .models import IngredientRecipe, Recipe, FavoriteRecipe


# from django.core import serializers


# ---------------------------------------
class PostIngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount")


# ---------------------------------------


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source="ingredients.id", queryset=Ingredient.objects.all()
    )
    measurement_unit = serializers.CharField(
        source="ingredients.measurement_unit", read_only=True
    )
    name = serializers.CharField(source="ingredients.name", read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
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


class ReadRecipeSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_tags(self, obj):
        recipe = get_object_or_404(Recipe, id=obj.id)
        tags = recipe.tags.all()
        return TagSerializer(tags, many=True).data

    def get_ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe_id=obj.id)
        return IngredientRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False


class ModRecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    ingredients = PostIngredientRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "ingredients",
            "author",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def to_representation(self, instance):
        request = self.context.get("request")
        serializer = ReadRecipeSerializer(
            instance, context={"request": request}
        )
        return serializer.data

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        tags_data = validated_data.pop("tags")
        validated_data["author"] = self.context["request"].user
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)

        for data in ingredients_data:
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredients=Ingredient.objects.get(id=data.get("id")),
                amount=data.get("amount"),
            )
        return recipe

    def update(self, instance, validated_data):
        if "ingredients" in validated_data:
            IngredientRecipe.objects.filter(recipe=instance).delete()
            ingredients_data = validated_data.pop("ingredients")

            for data in ingredients_data:
                IngredientRecipe.objects.create(
                    recipe=instance,
                    ingredients=Ingredient.objects.get(id=data.get("id")),
                    amount=data.get("amount"),
                )
        if "tags" in validated_data:
            tags_data = validated_data.pop("tags")
            instance.tags.set(tags_data)
        instance.image = validated_data.get("image", instance.image)
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )

        return instance


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteRecipe
        fields = (
            "recipe",
            "favorite",
        )
    
    def to_representation(self, instance):
        print(instance)
        print(self.context['request'])
        return ViewFavoriteShoppingcartRecipeSerializer(instance.recipe, context=self.context).data

class ViewFavoriteShoppingcartRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
