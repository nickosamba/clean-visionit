import datetime
from django.test import TestCase
from clients.forms import ClientForm
from clients.models import Client
from secteurs.models import Secteur, Rue
from abonnements.models import Abonnement, OptionService

class ClientFormTest(TestCase):
    def setUp(self):
        # Secteur et Rue
        self.secteur = Secteur.objects.create(nom="Secteur Test")
        self.rue = Rue.objects.create(
            nom="Rue Test",
            gps_lat=1.234567,
            gps_lon=2.345678,
            secteur=self.secteur
        )

        # Abonnement et Options
        self.abonnement = Abonnement.objects.create(nom="Base", montant_base=100)
        self.option1 = OptionService.objects.create(nom="Option1", prix_supplementaire=50)
        self.option2 = OptionService.objects.create(nom="Option2", prix_supplementaire=30)

    def test_valid_form_creates_client_with_options(self):
        form_data = {
            "prenom": "John",
            "nom": "Doe",
            "email": "john@example.com",
            "telephone_principal": "+123456789",
            "telephone_secondaire": "+987654321",
            "adresse_numero": "12B",
            "rue": self.rue.id,
            "abonnement": self.abonnement.id,
            "date_debut": "2026-01-01",
            "date_recouvrement": "2026-02-01",
            "statut": "Actif",
            "commentaires": "Client test",
            "gps_lat": 1.234567,
            "gps_lon": 2.345678,
            "options": [self.option1.id, self.option2.id],
        }
        form = ClientForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        client = form.save()  # 🔥 gère Client + Options + montant mensuel
        self.assertEqual(client.options.count(), 2)
        self.assertEqual(client.montant_mensuel, 180)  # 100 + 50 + 30

    def test_invalid_email(self):
        form_data = {
            "prenom": "Jane",
            "nom": "Smith",
            "email": "invalid-email",
            "telephone_principal": "+123456789",
            "rue": self.rue.id,
            "abonnement": self.abonnement.id,
            "date_recouvrement": "2026-02-01",
            "statut": "Actif",
        }
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_invalid_phone(self):
        form_data = {
            "prenom": "Alice",
            "nom": "Brown",
            "email": "alice@example.com",
            "telephone_principal": "123ABC",
            "rue": self.rue.id,
            "abonnement": self.abonnement.id,
            "date_recouvrement": "2026-02-01",
            "statut": "Actif",
        }
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("telephone_principal", form.errors)

    def test_date_format_html5(self):
        form_data = {
            "prenom": "Bob",
            "nom": "White",
            "email": "bob@example.com",
            "telephone_principal": "+123456789",
            "rue": self.rue.id,
            "abonnement": self.abonnement.id,
            "date_debut": "2026-01-01",  # format HTML5
            "date_recouvrement": "2026-02-01",
            "statut": "Actif",
        }
        form = ClientForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        client = form.save()
        self.assertEqual(client.date_debut, datetime.date(2026, 1, 1))
        self.assertEqual(client.date_recouvrement, datetime.date(2026, 2, 1))
