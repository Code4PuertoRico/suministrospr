from django.contrib import admin
from .models import Suministro


@admin.register(Suministro)
class SuministroAdmin(admin.ModelAdmin):
    pass
