from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag
from users.models import User


class Recipe(models.Model):
    """Модель рецепта."""

    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги",
        related_name="recipes",
    )

    author = models.ForeignKey(
        User,
        verbose_name="Авторы",
        related_name="recipes",
        on_delete=models.CASCADE,
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Ингредиенты",
        related_name="recipes",
        through="IngredientRecipe",
    )

    image = models.ImageField(
        "Фотография",
        help_text="Добавьте фотографию",
        upload_to="recipe/images/",
        blank=True,
    )

    name = models.CharField(
        "Наименование",
        help_text="Укажите наименование",
        max_length=200,
        error_messages={"max_length": "Значение более 200 символов"},
    )

    text = models.CharField(
        "Описание",
        max_length=1000,
        help_text="Добавьте описание",
    )

    cooking_time = models.IntegerField(
        "Время приготовления",
        help_text="Укажите время приготовления",
        validators=[
            MinValueValidator(
                1, message="Время приготовления не может быть менее 1 минуты"
            )
        ],
    )

    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredientrecipe",
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredientrecipe",
    )

    amount = models.SmallIntegerField(
        "Количество",
        help_text="Укажите количество ингредиента",
        validators=[
            MinValueValidator(1, message="Добавьте хотябы 1 ингредиент")
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            ),
        ]

    def __str__(self):
        return f"{self.ingredient} {self.recipe}"


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="Рецепт",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="Пользователь(добавитель в избранное)",
    )

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"],
                name="unique_recipe_favorite",
            ),
        ]

    def __str__(self):
        return f"{self.user} {self.recipe}"


class ShoppingcartRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Рецепт",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Пользователь(добавитель в корзину)",
    )

    class Meta:
        verbose_name = "Рецепт для добавленный в корзину"
        verbose_name_plural = "Рецепты в корзинах"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"],
                name="unique_recipe_shopping_cart",
            ),
        ]

    def __str__(self):
        return f"{self.user} {self.recipe}"
