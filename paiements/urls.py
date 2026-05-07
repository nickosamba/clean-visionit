from django.urls import path
from core import views

app_name = "paiement"

urlpatterns = [
    # Liste des paiements
    path("paiements/", views.paiements_list, name="paiements"),

    # Export
    path("export_pdf_mensuel/", views.export_pdf_mensuel, name="export_pdf_mensuel"),
]
