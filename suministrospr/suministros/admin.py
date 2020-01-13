from django.contrib import admin
from .models import Suministro


@admin.register(Suministro)
class SuministroAdmin(admin.ModelAdmin):
    list_display = ['title', 'municipality', 'created_at', 'modified_at']
