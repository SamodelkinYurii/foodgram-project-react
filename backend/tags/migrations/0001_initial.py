# Generated by Django 4.2.9 on 2024-01-09 17:13

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
                        error_messages={
                            "max_length": "Значение более 200 символов"
                        },
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
                        error_messages={
                            "max_length": "Значение более 200 символов",
                            "unique": "Значение не уникально",
                        },
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
                "ordering": ("name",),
            },
        ),
    ]
