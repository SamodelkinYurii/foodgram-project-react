from django.db import models


class Ingredient(models.Model):
    """Модель ингридиента."""

    name = models.CharField("Наименование", help_text="Укажите наименование", max_length=200, unique=True)
    measurement_unit = models.CharField("Единица измерения", help_text="Укажите единицу измерения", max_length=200)

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"
        ordering = ('name',)

    def __str__(self):
        return self.name
