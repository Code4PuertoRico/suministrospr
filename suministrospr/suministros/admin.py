from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Municipality, Suministro, Tag


@admin.register(Tag)
class TagAdmin(VersionAdmin):
    list_display = ["name", "slug"]


@admin.register(Municipality)
class MunicipalityAdmin(VersionAdmin):
    list_display = ["get_name", "slug", "created_at", "modified_at"]

    def get_name(self, obj):
        return obj.get_name_display()

    get_name.short_description = "name"


@admin.register(Suministro)
class SuministroAdmin(VersionAdmin):
    list_display = [
        "title",
        "slug",
        "municipality",
        "created_at",
        "modified_at",
    ]
