# Generated by Django 4.2.9 on 2024-01-10 12:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0008_shoppingcartrecipe_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="shoppingcartrecipe",
            options={
                "verbose_name": "Рецепт для добавленный в корзину",
                "verbose_name_plural": "Рецепты в корзинах",
            },
        ),
    ]