import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
from clients.models import Client, ClientOption
from secteurs.models import Secteur, Rue
from abonnements.models import Abonnement, OptionService

class ClientModelTest(TestCase):
    def setUp(self):
        # Créer un secteur obligatoire
        self.secteur = Secteur.objects.create(nom="Secteur Test")

        # Créer une rue liée au secteur
        self.rue = Rue.objects.create(
            nom="Rue Test",
            gps_lat=1.234567,
            gps_lon=2.345678,
            secteur=self.secteur
        )

        # Créer un abonnement et une option
        self.abonnement = Abonnement.objects.create(nom="Base", montant_base=100)
        self.option_service = OptionService.objects.create(nom="Option1", prix_supplementaire=50)

        # Date commune pour les tests
        self.date_recouvrement = datetime.date(2026, 1, 1)

    def test_str_and_full_name(self):
        client = Client.objects.create(
            nom="Doe",
            prenom="John",
            telephone_principal="+123456789",
            rue=self.rue,
            abonnement=self.abonnement,
            date_recouvrement=self.date_recouvrement
        )
        self.assertEqual(str(client), "Doe John")
        self.assertEqual(client.full_name(), "John Doe")

    def test_code_client_generated(self):
        client = Client.objects.create(
            nom="Smith",
            telephone_principal="+123456789",
            rue=self.rue,
            abonnement=self.abonnement,
            date_recouvrement=self.date_recouvrement
        )
        self.assertTrue(client.code_client.startswith("SMITH-"))

    def test_gps_inherited_from_rue(self):
        client = Client.objects.create(
            nom="Brown",
            telephone_principal="+123456789",
            rue=self.rue,
            abonnement=self.abonnement,
            date_recouvrement=self.date_recouvrement
        )
        self.assertEqual(client.gps_lat, self.rue.gps_lat)
        self.assertEqual(client.gps_lon, self.rue.gps_lon)

    def test_calculer_montant_mensuel(self):
        client = Client.objects.create(
            nom="White",
            telephone_principal="+123456789",
            rue=self.rue,
            abonnement=self.abonnement,
            date_recouvrement=self.date_recouvrement
        )
        ClientOption.objects.create(client=client, option=self.option_service)
        montant = client.calculer_montant_mensuel()
        self.assertEqual(montant, 150)
        self.assertEqual(client.montant_mensuel, 150)

    # 🔒 Tests de validation
    def test_invalid_email_raises_validation_error(self):
        client = Client(
            nom="InvalidEmail",
            telephone_principal="+123456789",
            rue=self.rue,
            abonnement=self.abonnement,
            email="invalid-email",
            date_recouvrement=self.date_recouvrement
        )
        with self.assertRaises(ValidationError):
            client.full_clean()

    def test_invalid_phone_raises_validation_error(self):
        client = Client(
            nom="InvalidPhone",
            telephone_principal="123ABC",
            rue=self.rue,
            abonnement=self.abonnement,
            date_recouvrement=self.date_recouvrement
        )
        with self.assertRaises(ValidationError):
            client.full_clean()

    def test_invalid_statut_raises_validation_error(self):
        client = Client(
            nom="InvalidStatut",
            telephone_principal="+123456789",
            rue=self.rue,
            abonnement=self.abonnement,
            statut="Pirate",
            date_recouvrement=self.date_recouvrement
        )
        with self.assertRaises(ValidationError):
            client.full_clean()
