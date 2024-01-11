from rest_framework import serializers

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


class SubscriptionSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
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
