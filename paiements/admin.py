from django.contrib import admin
from unfold.admin import ModelAdmin

# Register your models here.
from .models import Paiement, Recu, Echeance

@admin.register(Paiement)
class PaiementAdmin(ModelAdmin):
    list_display = ("echeance__client", "montant_paye", "date_paiement", "mode_paiement")
    search_fields = ("echeance__client__code_client", "echeance__client__nom", "echeance__client__prenom", "mode_paiement")
    list_filter = ("mode_paiement", "date_paiement")
    ordering = ("-date_paiement",)


@admin.register(Recu)
class RecuAdmin(ModelAdmin):
    list_display = ("paiement", "numero_recu", "date_creation")
    search_fields = ("numero_recu", "paiement__echeance__client__code_client")
    list_filter = ("date_creation",)
    ordering = ("-date_creation",)

@admin.register(Echeance)
class EcheanceAdmin(ModelAdmin):
    list_display = ("client", "montant_du", "date_echeance", "statut")
    search_fields = ("client__code_client", "client__nom", "client__prenom", "statut")
    list_filter = ("statut", "date_echeance")
    ordering = ("-date_echeance",)