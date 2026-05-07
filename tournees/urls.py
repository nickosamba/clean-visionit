from django.urls import path
from . import views
from . import api_views

app_name = "tournees"

urlpatterns = [
    path("", views.liste_tournees, name="tournees"),
    path("create/", views.create_tournee, name="create"),
    path("edit/<int:id>/", views.edit_tournee, name="edit"),
    path("delete/<int:id>/", views.delete_tournee, name="delete"),
    path("detail/<int:id>/", views.detail_tournee, name="detail"),

    # Gestion des clients dans une tournée
    path("<int:tournee_id>/clients/", views.liste_tournee_clients, name="liste_clients"),
    path("<int:tournee_id>/clients/add/", views.add_tournee_client, name="add_client"),
    path("<int:tournee_id>/clients/add-sector/", views.add_sector_clients_to_tournee, name="add_sector_clients"),
    path("clients/edit/<int:id>/", views.edit_tournee_client, name="edit_client"),
    path("clients/delete/<int:id>/", views.delete_tournee_client, name="delete_client"),

    # API endpoints
    path("api/check_assignments/", api_views.check_new_assignments, name="check_assignments"),
]


# from django.urls import path
# from . import views

# app_name = "tournees"

# urlpatterns = [
#     path("", views.tournees_view, name="tournees"),
#     path("planifier/", views.planifier_tournee, name="planifier"),
#     path("<int:tournee_id>/planifier-client/", views.planifier_tournee_client, name="planifier_client"),
#     path("<int:tournee_id>/supprimer/", views.supprimer_tournee, name="supprimer"), # ✅ ajout
# ]
