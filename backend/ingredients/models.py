from django.db import models


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        "Наименование",
        help_text="Укажите наименование",
        max_length=200,
        unique=True,
        error_messages={
            "max_length": "Значение более 200 символов",
            "unique": "Значение не уникально",
        },
    )
    measurement_unit = models.CharField(
        "Единица измерения",
        help_text="Укажите единицу измерения",
        max_length=200,
        error_messages={"max_length": "Значение более 200 символов"},
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)

    def __str__(self):
        return self.name
