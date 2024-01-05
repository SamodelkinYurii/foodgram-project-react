# Generated by Django 4.2.9 on 2024-01-05 12:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tags", "0003_auto_20240104_1102"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ingredients", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="IngredientRecipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.SmallIntegerField(
                        help_text="Укажите количество ингредиента",
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, message="Добавьте хотябы 1 ингредиент"
                            )
                        ],
                        verbose_name="Количество",
                    ),
                ),
                (
                    "ingredients",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ingredientrecipe",
                        to="ingredients.ingredient",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        help_text="Добавьте фотографию",
                        upload_to="recipe/images/",
                        verbose_name="Фотография",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        error_messages={"max_length": "Значение более 200 символов"},
                        help_text="Укажите наименование",
                        max_length=200,
                        verbose_name="Наименование",
                    ),
                ),
                (
                    "text",
                    models.CharField(
                        help_text="Добавьте описание",
                        max_length=1000,
                        verbose_name="Описание",
                    ),
                ),
                (
                    "cooking_time",
                    models.IntegerField(
                        help_text="Укажите время приготовления",
                        validators=[
                            django.core.validators.MinValueValidator(
                                1,
                                message="Время приготовления не может быть менее 1 минуты",
                            )
                        ],
                        verbose_name="Время приготовления",
                    ),
                ),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата публикации"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recipes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "ingredients",
                    models.ManyToManyField(
                        related_name="recipes",
                        through="recipes.IngredientRecipe",
                        to="ingredients.ingredient",
                        verbose_name="Ингридиенты",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Рецепт",
                "ordering": ("-pub_date",),
                "default_related_name": "Рецепты",
            },
        ),
        migrations.CreateModel(
            name="TagRecipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tagtrecipe",
                        to="recipes.recipe",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tagtrecipe",
                        to="tags.tag",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(
                related_name="recipes",
                through="recipes.TagRecipe",
                to="tags.tag",
                verbose_name="Теги",
            ),
        ),
        migrations.AddField(
            model_name="ingredientrecipe",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredientrecipe",
                to="recipes.recipe",
            ),
        ),
        migrations.AddConstraint(
            model_name="tagrecipe",
            constraint=models.UniqueConstraint(
                fields=("tag", "recipe"), name="unique_tag_recipe"
            ),
        ),
        migrations.AddConstraint(
            model_name="ingredientrecipe",
            constraint=models.UniqueConstraint(
                fields=("recipe", "ingredients"), name="unique_recipe_ingredients"
            ),
        ),
    ]
