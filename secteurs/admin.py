from django.contrib import admin
from .models import Secteur, Rue
from unfold.admin import ModelAdmin
# Register your models here.
@admin.register(Secteur)
class SecteurAdmin(ModelAdmin):
    list_display = ("nom", "description")
    search_fields = ("nom",)
    ordering = ("nom",)

@admin.register(Rue)
class RueAdmin(ModelAdmin):
    list_display = ("nom", "type_voie", "secteur")
    search_fields = ("nom", "secteur__nom")
    ordering = ("nom",)