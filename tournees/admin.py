from django.contrib import admin
from unfold.admin import ModelAdmin

# Register your models here.
from .models import Tournee, TourneeClient


@admin.register(Tournee)
class TourneeAdmin(ModelAdmin):
    list_display = ("agent", "date", "statut","secteur","heure_debut","heure_fin")
    search_fields = ("agent__user__email", "agent__user__username", "date", "statut")
    list_filter = ("statut", "date")
    ordering = ("-date",)

@admin.register(TourneeClient)
class TourneeClientAdmin(ModelAdmin):
    list_display = ("tournee", "client", "statut_service", "heure_passage","statut_service","commentaires_agent")
    search_fields = ("tournee__agent__user__email", "client__code_client", "statut_service")
    list_filter = ("statut_service",)
    ordering = ("tournee__date", "client__code_client")