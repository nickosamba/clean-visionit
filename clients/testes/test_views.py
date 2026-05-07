from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from clients.models import Client, ClientOption
from secteurs.models import Secteur, Rue
from abonnements.models import Abonnement, OptionService

User = get_user_model()

class ClientViewsIntegrationTest(TestCase):
    def setUp(self):
        # Utilisateur gestionnaire
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password",
            role="Gestionnaire"
        )
        self.user.is_staff = True
        self.user.save()
        self.client.login(email="testuser@example.com", password="password")

        # Données de base
        self.secteur = Secteur.objects.create(nom="Secteur Test")
        self.rue = Rue.objects.create(nom="Rue Test", secteur=self.secteur)
        self.abonnement = Abonnement.objects.create(nom="Base", montant_base=100)
        self.option1 = OptionService.objects.create(nom="Option1", prix_supplementaire=50)

        # Client initial
        self.client_obj = Client.objects.create(
            prenom="Jane",
            nom="Smith",
            email="jane@example.com",
            telephone_principal="+987654321",
            rue=self.rue,
            abonnement=self.abonnement,
            date_recouvrement="2026-02-01",
            statut="Actif",
            montant_mensuel=150,
        )
        ClientOption.objects.create(client=self.client_obj, option=self.option1, valeur="Active")

    def test_client_list_view(self):
        url = reverse("clients:liste")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SMITH Jane")
        self.assertContains(response, "Base")

    def test_client_details_view(self):
        url = reverse("clients:details", args=[self.client_obj.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Vérifier le nom complet tel qu'affiché dans le template
        self.assertContains(response, "SMITH Jane")

        # Vérifier l'email
        self.assertContains(response, "jane@example.com")

        # Vérifier l'abonnement
        self.assertContains(response, "Base")

        # Vérifier le statut
        self.assertContains(response, "Actif")


    def test_client_create_view(self):
        url = reverse("clients:create")
        data = {
            "prenom": "John",
            "nom": "Doe",
            "email": "john@example.com",
            "telephone_principal": "+123456789",
            "adresse_numero": "12B",
            "rue": self.rue.id,
            "abonnement": self.abonnement.id,
            "date_debut": "2026-01-01",
            "date_recouvrement": "2026-02-01",
            "statut": "Actif",
            "gps_lat": 1.234567,
            "gps_lon": 2.345678,
            "options": [self.option1.id],
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Client.objects.filter(nom="Doe").exists())

    def test_client_update_view(self):
        url = reverse("clients:update", args=[self.client_obj.id])
        data = {
            "prenom": "Jane",
            "nom": "Smith",
            "email": "jane_updated@example.com",
            "telephone_principal": "+987654321",
            "rue": self.rue.id,
            "abonnement": self.abonnement.id,
            "date_debut": "2026-01-01",
            "date_recouvrement": "2026-02-01",
            "statut": "Actif",
            "options": [self.option1.id],
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.client_obj.refresh_from_db()
        self.assertEqual(self.client_obj.email, "jane_updated@example.com")

    def test_client_delete_view(self):
        url = reverse("clients:delete", args=[self.client_obj.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Client.objects.filter(id=self.client_obj.id).exists())

    def test_export_clients_excel(self):
        url = reverse("clients:export_excel")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def test_export_clients_pdf(self):
        url = reverse("clients:export_pdf")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
