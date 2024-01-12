from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from ingredients.models import Ingredient
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserSerializer

from .exceptions import AuthorPermissionDenied
from .models import (
    FavoriteRecipe,
    IngredientRecipe,
    Recipe,
    ShoppingcartRecipe,
)


class PostIngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount")


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
        current_user = self.context["request"].user
        if not current_user.is_anonymous:
            return obj.favorite.filter(
                recipe=obj.id, favorite=current_user
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context["request"].user
        if not current_user.is_anonymous:
            return obj.shopping_cart.filter(
                recipe=obj.id, shoppingcart=current_user
            ).exists()
        return False


class ModRecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    ingredients = PostIngredientRecipeSerializer(many=True)
    image = Base64ImageField(required=True)

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
        if instance.author != self.context["request"].user:
            raise AuthorPermissionDenied()
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

    def validate(self, data):
        tags = data.get("tags")
        if not data.get("ingredients"):
            raise serializers.ValidationError(
                "Поле ingredients не может быть пустым"
            )
        if not tags:
            raise serializers.ValidationError("Поле tags не может быть пустым")
        if not data.get("image"):
            raise serializers.ValidationError(
                "Поле image не может быть пустым"
            )
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                "Поле tags не может дублироватся"
            )
        ingredients = [
            ingredient.get("id") for ingredient in data.get("ingredients")
        ]
        if len(ingredients) != len(set(ingredients)):
            raise serializers.ValidationError(
                "Поле ingredients не может дублироватся"
            )
        ingredients_bd_list = list(
            Ingredient.objects.all().values_list("id", flat=True)
        )
        if not all(x in ingredients_bd_list for x in ingredients):
            raise serializers.ValidationError("Добавте ingredients в базу")
        return data


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = (
            "recipe",
            "favorite",
        )

    def to_representation(self, instance):
        return ViewRecipeSerializerViewRecipeSerializer(
            instance.recipe, context=self.context
        ).data


class ShoppingcartRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingcartRecipe
        fields = (
            "recipe",
            "shoppingcart",
        )

    def to_representation(self, instance):
        return ViewRecipeSerializerViewRecipeSerializer(
            instance.recipe, context=self.context
        ).data


class ViewRecipeSerializerViewRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )
