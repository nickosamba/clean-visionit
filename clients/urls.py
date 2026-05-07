from django.urls import path
from . import views

app_name = "clients"

urlpatterns = [
    path("", views.client_list, name="liste"),
    path("ajouter/", views.client_create, name="create"),
    path("<int:id>/modifier/", views.client_update, name="update"),
    path("<int:id>/details/", views.client_details, name="details"),
    path("<int:id>/supprimer/", views.client_delete, name="delete"),
    path("export/excel/", views.export_clients_excel, name="export_excel"),
    path("export/pdf/", views.export_clients_pdf, name="export_pdf"),
    path("<int:client_id>/export_pdf/", views.exporter_pdf_client, name="export_pdf"),

]

# app_name = "clients"

# urlpatterns = [
# 
#     path("<int:id>/details/", views.client_details, name="details"),
#     path("<int:id>/modifier/", views.client_update, name="modifier"),
#     path("<int:id>/supprimer/", views.client_delete, name="supprimer"),
#     path("export/excel/", views.export_clients_excel, name="export_excel"),
#     path("export/pdf/", views.export_clients_pdf, name="export_pdf"),
# ]
