from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from ingredients.models import Ingredient
from recipes.models import (
    FavoriteRecipe,
    IngredientRecipe,
    Recipe,
    ShoppingcartRecipe,
)
from tags.models import Tag
from users.models import Subscribe, User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "color",
            "slug",
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
        )


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        return all(
            (
                (not user.is_anonymous),
                obj.subscriber.filter(
                    user=user.id, subscriber=obj.id
                ).exists(),
            )
        )


class SubscribeSerializer(UserSerializer):
    class Meta:
        model = Subscribe
        fields = (
            "user",
            "subscriber",
        )

    def validate(self, data):
        if data["user"] == data["subscriber"]:
            raise serializers.ValidationError(
                {"detail": "Нельзя подписатся на себя"}
            )
        if Subscribe.objects.filter(
            user=data["user"], subscriber=data["subscriber"]
        ).exists():
            raise ValidationError(
                {"detail": "Вы уже подписанны на данного автора"}
            )
        return data

    def to_representation(self, instance):
        return SubscriptionSerializer(instance.user, context=self.context).data


class SubscriptionSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source="recipes.count")

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_recipes(self, obj):
        request = self.context["request"]
        limit = request.GET.get("recipes_limit")
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[: int(limit)]
        serializer = ViewRecipeSerializer(recipes, many=True, read_only=True)
        return serializer.data


class ViewRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class PostIngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount")


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source="ingredient.id", queryset=Ingredient.objects.all()
    )
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit", read_only=True
    )
    name = serializers.CharField(source="ingredient.name", read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class ReadRecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True,
        source="ingredientrecipe",
    )
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

    def get_is_favorited(self, obj):
        current_user = self.context["request"].user
        if not current_user.is_anonymous:
            return obj.favorite.filter(
                recipe=obj.id, user=current_user
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context["request"].user
        if not current_user.is_anonymous:
            return obj.shopping_cart.filter(
                recipe=obj.id, user=current_user
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

    @staticmethod
    def create_ingredients(ingredients_data, recipe):
        IngredientRecipe.objects.bulk_create(
            IngredientRecipe(
                recipe=recipe,
                ingredient_id=data.get("id"),
                amount=data["amount"],
            )
            for data in ingredients_data
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        tags_data = validated_data.pop("tags")
        validated_data["author"] = self.context["request"].user
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        if "ingredients" in validated_data:
            IngredientRecipe.objects.filter(recipe=instance).delete()
            ingredients_data = validated_data.pop("ingredients")
            self.create_ingredients(ingredients_data, instance)
        if "tags" in validated_data:
            tags_data = validated_data.pop("tags")
            instance.tags.set(tags_data)
        return super().update(instance, validated_data)

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
            "user",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteRecipe.objects.all(),
                fields=("recipe", "user"),
                message="Вы уже добавили рецепт в избранное",
            )
        ]

    def to_representation(self, instance):
        return ViewRecipeSerializerViewRecipeSerializer(
            instance.recipe, context=self.context
        ).data


class ShoppingcartRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingcartRecipe
        fields = (
            "recipe",
            "user",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingcartRecipe.objects.all(),
                fields=("recipe", "user"),
                message="Вы уже добавили рецепт в корзину",
            )
        ]

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
