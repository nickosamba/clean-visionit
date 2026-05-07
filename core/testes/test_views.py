from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from paiements.models import Echeance, Paiement
from clients.models import Client
from secteurs.models import Secteur
from abonnements.models import Abonnement
from unittest.mock import patch

User = get_user_model()

class CoreViewsIntegrationTest(TestCase):
    def setUp(self):
        # Admin superuser pour dashboard global
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
            role="Administrateur"
        )

        # Admin non-superuser pour user_detail
        self.admin_user = User.objects.create_user(
            username="admin_user",
            email="admin_user@example.com",
            password="password",
            role="Admin",
            is_staff=True,
            is_superuser=False
        )

        # Comptable
        self.comptable = User.objects.create_user(
            username="comptable",
            email="comptable@example.com",
            password="password",
            role="Comptable",
            is_staff=True
        )

        # Gestionnaire
        self.gestionnaire = User.objects.create_user(
            username="gestionnaire",
            email="gest@example.com",
            password="password",
            role="Gestionnaire",
            is_staff=True
        )

        # Données de base
        self.secteur = Secteur.objects.create(nom="Secteur Test")
        self.abonnement = Abonnement.objects.create(nom="Base", montant_base=100)
        self.client_obj = Client.objects.create(
            prenom="Jane",
            nom="Smith",
            email="jane@example.com",
            telephone_principal="+987654321",
            rue=None,
            abonnement=self.abonnement,
            date_recouvrement="2026-02-01",
            statut="Actif",
            montant_mensuel=100,
        )

        self.echeance = Echeance.objects.create(
            client=self.client_obj,
            montant_du=100,
            statut=Echeance.Statut.A_PAYER,
            date_echeance=date.today()
        )

    # ------------------- Tests Admin -------------------
    def test_dashboard_admin_view(self):
        self.client.login(email="admin@example.com", password="password")
        response = self.client.get(reverse("dashboard:admin"))
        self.assertEqual(response.status_code, 200)

    def test_users_list_view(self):
        self.client.login(email="admin@example.com", password="password")
        response = self.client.get(reverse("dashboard:users_list"))
        self.assertEqual(response.status_code, 200)

    def test_user_detail_view(self):
        self.client.login(email="admin@example.com", password="password")
        response = self.client.get(reverse("dashboard:user_detail", args=[self.admin_user.id]))
        self.assertEqual(response.status_code, 200)

    # ------------------- Tests Comptable -------------------
    def test_dashboard_comptable_view(self):
        self.client.login(email="comptable@example.com", password="password")
        response = self.client.get(reverse("dashboard:comptable"))
        self.assertEqual(response.status_code, 200)

    def test_echeances_list_view(self):
        self.client.login(email="comptable@example.com", password="password")
        response = self.client.get(reverse("dashboard:echeances"))
        self.assertEqual(response.status_code, 200)

    def test_payer_echeance_view(self):
        self.client.login(email="comptable@example.com", password="password")
        url = reverse("dashboard:payer_echeance", args=[self.echeance.id])
        data = {"montant_paye": 100, "mode_paiement": Paiement.Mode.ESPECES}
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.echeance.refresh_from_db()
        self.assertEqual(self.echeance.statut, Echeance.Statut.PAYE)

    def test_export_excel_mensuel_view(self):
        self.client.login(email="comptable@example.com", password="password")
        response = self.client.get(reverse("dashboard:export_excel_mensuel"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def test_export_pdf_mensuel_view(self):
        self.client.login(email="comptable@example.com", password="password")
        response = self.client.get(reverse("dashboard:export_pdf_mensuel"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    # ------------------- Tests Gestionnaire -------------------
    def test_dashboard_gestionnaire_view(self):
        self.client.login(email="gest@example.com", password="password")
        response = self.client.get(reverse("dashboard:gestionnaire"))
        self.assertEqual(response.status_code, 200)


    

    def test_export_tournees_pdf_view(self):
        self.client.login(email="gest@example.com", password="password")
        with patch("core.views.render_to_string", return_value="<html><body>dummy</body></html>"):
            response = self.client.get(reverse("dashboard:export_pdf"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")


    def test_export_tournees_excel_view(self):
        self.client.login(email="gest@example.com", password="password")
        response = self.client.get(reverse("dashboard:export_excel"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def test_export_agents_excel_view(self):
        self.client.login(email="gest@example.com", password="password")
        response = self.client.get(reverse("dashboard:export_agents"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
