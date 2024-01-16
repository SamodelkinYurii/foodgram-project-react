from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ["name"]
