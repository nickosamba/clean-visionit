from django.urls import path
from . import views

app_name = "abonnements"

urlpatterns = [
    # Abonnements
    path("", views.liste_abonnements, name="liste"),
    path("create/", views.create_abonnement, name="create"),
    path("edit/<int:id>/", views.edit_abonnement, name="edit"),
    path("detail/<int:id>/", views.detail_abonnement, name="detail"),
    path("delete/<int:id>/", views.delete_abonnement, name="delete_abonnement"),

    path("historique/", views.historique_tarifs, name="historique"),

    # Options
    path("options/", views.liste_options, name="liste_options"),
    path("options/create/", views.create_option_global, name="create_option_global"),
    path("options/create/<int:abonnement_id>/", views.create_option, name="create_option"),
    path("options/edit/<int:id>/", views.edit_option, name="edit_option"),
    path("options/delete/<int:id>/", views.delete_option, name="delete_option"),

]