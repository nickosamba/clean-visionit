from django.urls import path
from . import views

app_name = "agents"

urlpatterns = [
    path("", views.agent_list, name="liste"),
    path("<int:agent_id>/", views.agent_detail, name="detail_agent"),
    path("ajouter/", views.agent_create, name="ajouter"),
    path("export/", views.export_agents_excel, name="export_excel"),
    path("export/pdf/", views.export_agents_pdf, name="export_pdf"),
    path("<int:agent_id>/modifier/", views.agent_update, name="modifier"),
    path("delete/<int:agent_id>/", views.agent_delete, name="delete_agent"),
    # Export PDF d’un agent spécifique 
    path("<int:agent_id>/export_pdf/", views.exporter_pdf_agent, name="export_pdf"),

    #incidents
    path("incident/", views.liste_incidents, name="liste_incidents"),
    #path("create/", views.create_incident, name="create"),
    #path("edit/<int:id>/", views.edit_incident, name="edit"),
    path("incident/delete/<int:id>/", views.delete_incident, name="delete_incident"),
    path("incident/detail/<int:id>/", views.detail_incident, name="detail_incident"),
]

