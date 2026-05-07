from django.contrib import admin
from unfold.admin import ModelAdmin

# Register your models here.
from .models import Abonnement, TarifHistorique, OptionService

@admin.register(Abonnement)
class AbonnementAdmin(ModelAdmin):
    list_display = ("nom", "montant_base", "avantages", "description")
    search_fields = ("nom", "montant_base", "avantages")
    list_filter = ("nom", "montant_base")
    ordering = ("-created_at",)

@admin.register(TarifHistorique)
class TarifHistoriqueAdmin(ModelAdmin):
    list_display = ("abonnement", "ancien_montant", "nouveau_montant","date_changement")
    search_fields = ("abonnement__client__code_client", "abonnement__client__nom")
    list_filter = ("date_changement",)
    ordering = ("-date_changement",)


@admin.register(OptionService)
class OptionServiceAdmin(ModelAdmin):
    list_display = ("nom", "prix_supplementaire", "statut")
    search_fields = ("nom", "description")
    list_filter = ("statut",)
    ordering = ("-created_at",)
