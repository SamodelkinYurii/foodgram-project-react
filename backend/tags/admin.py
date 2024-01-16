from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Tag


@admin.register(Tag)
class TagAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ("name", "color", "slug")
