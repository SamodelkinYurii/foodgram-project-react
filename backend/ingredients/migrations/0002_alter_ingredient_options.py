# Generated by Django 3.2.16 on 2024-01-16 06:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ingredients", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ingredient",
            options={
                "ordering": ("name",),
                "verbose_name": "Ингредиент",
                "verbose_name_plural": "Ингредиенты",
            },
        ),
    ]
