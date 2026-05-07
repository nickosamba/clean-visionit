from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin
# Register your models here.
from .models import Agent, Secteur, Incident

class AgentAdmin(ModelAdmin):
    list_display = ("user","secteur", "telephone_principal", "adresse", "date_embauche", "statut", "change_user_link")
    search_fields = ("user__email", "user__username", "telephone", "adresse")
    list_filter = ("statut", "date_embauche")
    ordering = ("user__email",)
    readonly_fields = ("matricule", "change_user_link")  # Make matricule read-only since it's auto-generated

    def change_user_link(self, obj):
        if obj.user:
            url = reverse('admin:accounts_user_change', args=[obj.user.pk])
            return format_html('<a href="{}" class="button">Modifier le profil utilisateur</a>', url)
        return "Aucun utilisateur associé"
    change_user_link.short_description = "Profil utilisateur"

    def get_fieldsets(self, request, obj=None):
        if obj:  # Editing an existing object
            return (
                ("Informations Agent", {
                    "fields": ("user", "secteur", "matricule", "zone_intervention", "statut",
                              "date_embauche", "type_contrat", "telephone_principal",
                              "telephone_secondaire", "adresse", "photo_profile")
                }),
                ("Actions", {
                    "fields": ("change_user_link",),
                    "classes": ("collapse",)  # Make this section collapsible
                }),
            )
        return (
            ("Informations Agent", {
                "fields": ("user", "secteur", "zone_intervention", "statut",
                          "date_embauche", "type_contrat", "telephone_principal",
                          "telephone_secondaire", "adresse", "photo_profile")
            }),
        )

admin.site.register(Agent, AgentAdmin)


@admin.register(Incident)
class IncidentAdmin(ModelAdmin):
    list_display = ("type_incident", "agent", "client", "date_signalement")
    search_fields = ("type_incident", "agent__user__email", "client__code_client")
    list_filter = ("type_incident",)
    ordering = ("-date_signalement",)
