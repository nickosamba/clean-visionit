import datetime
from django.test import TestCase
from clients.models import Client, ClientOption
from secteurs.models import Secteur, Rue
from abonnements.models import Abonnement, OptionService

class ClientOptionModelTest(TestCase):
    def setUp(self):
        # Secteur et Rue
        self.secteur = Secteur.objects.create(nom="Secteur Test")
        self.rue = Rue.objects.create(
            nom="Rue Test",
            gps_lat=1.234567,
            gps_lon=2.345678,
            secteur=self.secteur
        )

        # Abonnement et Option
        self.abonnement = Abonnement.objects.create(nom="Base", montant_base=100)
        self.option_service = OptionService.objects.create(nom="Option1", prix_supplementaire=50)

        # Client
        self.client = Client.objects.create(
            nom="Doe",
            prenom="John",
            telephone_principal="+123456789",
            rue=self.rue,
            abonnement=self.abonnement,
            date_recouvrement=datetime.date(2026, 1, 1)
        )

    def test_str_representation(self):
        client_option = ClientOption.objects.create(
            client=self.client,
            option=self.option_service,
            valeur="Active"
        )
        self.assertEqual(
            str(client_option),
            f"{self.client} - {self.option_service.nom} : Active"
        )

    def test_relation_with_client_and_option(self):
        client_option = ClientOption.objects.create(
            client=self.client,
            option=self.option_service
        )
        self.assertEqual(client_option.client, self.client)
        self.assertEqual(client_option.option, self.option_service)
