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
    id = serializers.PrimaryKeyRelatedField(
        source="subscriber.id", queryset=User.objects.all()
    )
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    email = serializers.EmailField(source="subscriber.email", read_only=True)
    first_name = serializers.ReadOnlyField(
        source="subscriber.first_name",
    )
    last_name = serializers.ReadOnlyField(
        source="subscriber.last_name",
    )
    username = serializers.ReadOnlyField(
        source="subscriber.username",
    )

    class Meta:
        model = Subscribe
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            # 'is_subscribed',
            # 'recipes',
            # 'recipes_count',
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
