from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Suministro, Tag


@admin.register(Tag)
class TagAdmin(VersionAdmin):
    list_display = ["name", "slug"]


@admin.register(Suministro)
class SuministroAdmin(VersionAdmin):
    list_display = [
        "title",
        "slug",
        "municipality",
        "created_at",
        "modified_at",
    ]
