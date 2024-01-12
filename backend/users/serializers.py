from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Recipe

from .models import Subscribe, User


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
            raise serializers.ValidationError("Нельзя подписатся на себя")
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
        request = self.context.get("request")
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
