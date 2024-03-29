from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name", "password")

    email = models.EmailField(
        "Почта",
        help_text="Укажите почту",
        max_length=254,
        unique=True,
        error_messages={
            "max_length": "Значение более 254 символовов",
            "unique": "Значение не уникально",
        },
    )
    username = models.CharField(
        "Логин",
        help_text="Введите логин",
        max_length=150,
        validators=(ASCIIUsernameValidator(),),
        unique=True,
        error_messages={
            "max_length": "Значение более 150 символовов",
            "unique": "Значение не уникально",
        },
    )
    first_name = models.CharField(
        "Имя",
        help_text="Введите имя",
        max_length=150,
        error_messages={"max_length": "Значение более 150 символовов"},
    )
    last_name = models.CharField(
        "Фамилия",
        help_text="Введите фамилию",
        max_length=150,
        error_messages={"max_length": "Значение более 150 символовов"},
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("email",)

    def __str__(self):
        return self.email


class Subscribe(models.Model):
    """Модель связи пользователей и подписчиков."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="Текущий пользователь",
    )

    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriber",
        verbose_name="Пользователь на которого сделана подписка",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "subscriber"],
                name="unique_user_subscriber",
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F("subscriber")),
                name="Подписаться на самого себя нельзя",
            ),
        ]

    def __str__(self):
        return f"{self.user} {self.subscriber}"
