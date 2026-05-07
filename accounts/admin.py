from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import UserCreationForm, UserChangeForm
from .models import User, AuditLog

admin.site.site_header = "CLEAN Administration"
admin.site.site_title = "CLEAN Admin Portal"
admin.site.index_title = "Bienvenue sur le portail d'administration CLEAN"

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Use Unfold forms for better styling
    add_form = UserCreationForm
    form = UserChangeForm

    # Colonnes visibles dans la liste
    list_display = ("email", "username", "role", "is_active", "is_staff", "deux_facteurs_active")
    list_filter = ("role", "is_active", "is_staff", "deux_facteurs_active")

    # Recherche
    search_fields = ("email", "username", "role")
    ordering = ("email",)

    # Champs affichés dans le formulaire d’édition
    fieldsets = (
        ("Informations personnelles", {
            "fields": ("email", "username", "first_name", "last_name", "role", "password")
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Sécurité", {
            "fields": ("deux_facteurs_active",)
        }),
        ("Dates importantes", {
            "fields": ("last_login", "date_joined")
        }),
    )

    # Champs affichés lors de la création d’un utilisateur
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "role", "password1", "password2"),
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(ModelAdmin):
    list_display = ("utilisateur", "action", "entite", "entite_id", "date_action")
    list_filter = ("action", "entite")
    search_fields = ("utilisateur__email", "action", "entite")
    ordering = ("-date_action",)