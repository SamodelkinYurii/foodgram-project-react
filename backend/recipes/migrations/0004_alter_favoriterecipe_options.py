# Generated by Django 4.2.9 on 2024-01-09 19:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0003_favoriterecipe_favoriterecipe_unique_recipe_favorite"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="favoriterecipe",
            options={"verbose_name_plural": "Избранные рецепты"},
        ),
    ]
