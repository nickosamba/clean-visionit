from django.urls import path
from . import views

app_name = "secteurs"

urlpatterns = [
    # Secteurs
    path("", views.liste_secteurs, name="liste"),
    path("create/", views.create_secteur, name="create"),
    path("edit/<int:id>/", views.edit_secteur, name="edit"),
    path("delete/<int:id>/", views.delete_secteur, name="delete"),
    path("detail/<int:id>/", views.detail_secteur, name="detail"),

     # Rues
    path("rues/", views.liste_rues, name="liste_rues"),
    path("rues/create/", views.create_rue_global, name="create_rue_global"),
    path("rues/create/<int:secteur_id>/", views.create_rue, name="create_rue"),
    path("rues/edit/<int:id>/", views.edit_rue, name="edit_rue"),
    path("rues/delete/<int:id>/", views.delete_rue, name="delete_rue"),
]









# # secteurs/urls.py
# from django.urls import path
# from . import views

# app_name = "secteurs"

# urlpatterns = [
#     path("", views.secteurs_view, name="liste"),

#     # Secteurs
#     path("ajouter/", views.ajouter_secteur, name="ajouter"),
#     path("<int:secteur_id>/modifier/", views.modifier_secteur, name="modifier"),
#     path("<int:secteur_id>/supprimer/", views.supprimer_secteur, name="supprimer"),

#     # Rues
#     path("rues/ajouter/", views.ajouter_rue, name="ajouter_rue"),
#     path("rues/<int:rue_id>/modifier/", views.modifier_rue, name="modifier_rue"),
#     path("rues/<int:rue_id>/supprimer/", views.supprimer_rue, name="supprimer_rue"),
# ]
