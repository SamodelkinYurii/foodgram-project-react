# Generated by Django 3.2.16 on 2024-01-17 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_auto_20240116_0937'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favoriterecipe',
            name='unique_recipe_favorite',
        ),
        migrations.RenameField(
            model_name='favoriterecipe',
            old_name='favorite',
            new_name='user',
        ),
        migrations.AddConstraint(
            model_name='favoriterecipe',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='unique_recipe_user'),
        ),
    ]