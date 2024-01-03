# Generated by Django 3.2.16 on 2024-01-03 13:34

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                    "name",
                    models.CharField(
                        help_text="Укажите наименование",
                        max_length=200,
                        verbose_name="Наименование",
                    ),
                ),
                (
                    "color",
                    colorfield.fields.ColorField(
                        default="#FFFFFF",
                        help_text="Укажите цвет",
                        image_field=None,
                        max_length=7,
                        samples=None,
                        verbose_name="Цвет",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Укажите слаг, поле должно быть уникальным",
                        max_length=200,
                        unique=True,
                        verbose_name="Слаг",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
            },
        ),
    ]