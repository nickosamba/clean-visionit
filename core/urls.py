from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # path("", views.dashboard_router, name="dashborad_router"),
    path("admin/", views.dashboard_admin, name="admin"),
    path("gestionnaire/", views.dashboard_gestionnaire, name="gestionnaire"),
    path("incidents/", views.incidents_view, name="incidents"),
    path("incidents/<int:incident_id>/traiter/", views.traiter_incident, name="traiter_incident"),
    path("export/pdf/", views.export_tournees_pdf, name="export_pdf"),
    path("export/excel/", views.export_tournees_excel, name="export_excel"), 
    path("export/agents/", views.export_agents_excel, name="export_agents"), 
    # path("tournees/", views.tournees_view, name="tournees"),
    # path("planifier/", views.planifier_tournee, name="planifier"),
    # path("<int:tournee_id>/planifier-client/", views.planifier_tournee_client, name="planifier_client"),
    #path("incidents/", views.incidents_view, name="incidents"),


    path("agent/", views.dashboard_agent, name="agent"),
    path("agent/profile/", views.agent_profile, name="agent_profile"),
    path("agent/incident/", views.agent_incident, name="agent_incident"),
    path("agent/confirmer/<int:tc_id>/", views.confirmer_passage, name="confirmer_passage"),
    path("agent/signaler/<int:tc_id>/", views.signaler_passage, name="signaler_passage"), # <-- ajout
    # API endpoints
    path('api/toggle-theme/', views.toggle_theme, name='toggle_theme'),  # Toggle theme API endpoint
    
    #comptable
    path("comptable/", views.dashboard_comptable, name="comptable"),
    path("echeances/", views.echeances_list, name="echeances"),
    # Payer une échéance 
    path("echeances/<int:echeance_id>/payer/", views.payer_echeance, name="payer_echeance"),
    path("export_pdf_mensuel/", views.export_pdf_mensuel, name="export_pdf_mensuel"),
    path("export_excel_mensuel/", views.export_excel_mensuel, name="export_excel_mensuel"),
    # Paiements 
    #path("paiement/<int:echeance_id>/", views.creer_paiement, name="paiement"),
    # Liste des paiements 
    path("paiements/", views.paiements_list, name="paiements"),
    path("export_pdf/", views.paiements_pdf, name="export_pdf"),
    path("recus/", views.recu_list, name="recu_list"),
    path("recu/<int:paiement_id>/pdf/", views.recu_pdf, name="recu_pdf"),
    #path("recu/<int:paiement_id>/", views.recu_pdf, name="recu_pdf"),

    #admin
    path('admin/summary/', views.dashboard_admin, name='dashboard_admin_summary'),
    path("admin/users/", views.users_list, name="users_list"),
    path("admin/comptes/<int:user_id>/", views.user_detail, name="user_detail"),
    path("admin/comptes/<int:user_id>/modifier/", views.user_edit, name="user_edit"),
    path("admin/comptes/<int:user_id>/toggle-active/", views.user_toggle_active, name="user_toggle_active"),
    path("admin/comptes/<int:user_id>/supprimer/", views.user_delete, name="user_delete"),
    path("admin/comptes/<int:user_id>/password/", views.user_change_password, name="user_change_password"),


    path("salaires/", views.salaires_list, name="salaires"),
    path("salaires/generer/", views.generer_salaires_mensuels_view, name="generer_salaires"),
    # Export PDF global des salaires path
    path("export_pdf_salaire/", views.salaires_pdf, name="export_pdf_salaire"),
    path("salaires/ajouter/", views.ajouter_salaire, name="ajouter_salaire"),
    path("salaires/payer/<int:salaire_id>/", views.payer_salaire, name="payer_salaire"),

    #path("ex

]
