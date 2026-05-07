from django.contrib import admin
from .models import Client, ClientOption
from unfold.admin import ModelAdmin

@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ("code_client", "nom", "prenom", "telephone_principal", "statut")

    list_filter = ("statut", "abonnement", "date_recouvrement")
    search_fields = ("code_client", "nom", "prenom", "telephone_principal")
    ordering = ("nom", "prenom")


@admin.register(ClientOption)
class ClientOptionAdmin(ModelAdmin):
    list_display = ("client", "option", "valeur", "created_at")
    list_filter = ("option",)
