from colorfield.fields import ColorField
from django.db import models


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        "Наименование", help_text="Укажите наименование", max_length=200
    )
    color = ColorField("Цвет", help_text="Укажите цвет", max_length=7)
    slug = models.SlugField(
        "Слаг",
        help_text="Укажите слаг, поле должно быть уникальным",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ('name',)

    def __str__(self):
        return self.name
