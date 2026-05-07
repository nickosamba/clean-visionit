from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from clients.models import Client, ClientOption
from secteurs.models import Secteur, Rue
from abonnements.models import Abonnement, OptionService

User = get_user_model()

class ClientCreateIntegrationTest(TestCase):
    def setUp(self):
        # Créer un utilisateur gestionnaire
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
        self.option2 = OptionService.objects.create(nom="Option2", prix_supplementaire=30)

    def test_create_client_via_view(self):
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
            "options": [self.option1.id, self.option2.id],
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Vérifier que le client est créé
        client = Client.objects.get(nom="Doe")
        self.assertEqual(client.prenom, "John")
        self.assertEqual(client.email, "john@example.com")
        self.assertEqual(client.statut, "Actif")
        self.assertEqual(client.abonnement, self.abonnement)
        self.assertEqual(client.rue, self.rue)

        # Vérifier les options et le montant mensuel
        self.assertEqual(client.options.count(), 2)
        self.assertEqual(client.montant_mensuel, 180)  # 100 + 50 + 30

        # Vérifier que la vue redirige vers la liste des clients
        self.assertRedirects(response, reverse("clients:liste"))

    def test_client_list_view_shows_created_client(self):
        client = Client.objects.create(
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

        url = reverse("clients:liste")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Vérifier que le nom apparaît (adapter à ton rendu HTML)
        self.assertContains(response, "SMITH Jane")
        # Vérifier l’abonnement
        self.assertContains(response, "Base")
