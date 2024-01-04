from django.contrib import admin

from .models import Subscribe, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
    )
    list_filter = ["email", "username"]


@admin.register(Subscribe)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subscriber",
    )
