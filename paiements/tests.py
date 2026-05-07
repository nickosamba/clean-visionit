from django.test import TestCase
from django.utils import timezone
from clients.models import Client
from paiements.models import Echeance, Paiement

class EcheanceModelTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            nom="Nicko", 
            montant_mensuel=30000,
            telephone_principal="+242066000000",
            date_recouvrement=timezone.now().date()
        )
        self.echeance = Echeance.objects.create(
            client=self.client,
            montant_du=30000,
            periode="2026-01",
            type_echeance=Echeance.Type.MENSUELLE
        )

    def test_reste_a_payer_initial(self):
        self.assertEqual(self.echeance.reste_a_payer, 30000)

    def test_reste_a_payer_apres_paiement(self):
        Paiement.objects.create(
            echeance=self.echeance, 
            montant_paye=10000,
            date_paiement=timezone.now()
        )
        self.assertEqual(self.echeance.reste_a_payer, 20000)

class EcheancePaiementTest(TestCase):

    def setUp(self):
        # Création d’un client avec les champs obligatoires
        self.client = Client.objects.create(
            nom="Nicko", 
            montant_mensuel=30000,
            telephone_principal="+242066000000",
            date_recouvrement=timezone.now().date()
        )
        # Création d’une échéance liée
        self.echeance = Echeance.objects.create(
            client=self.client,
            montant_du=30000,
            periode="2026-01",
            type_echeance=Echeance.Type.MENSUELLE,
            statut=Echeance.Statut.A_PAYER
        )

    def test_paiement_partiel(self):
        """Un paiement partiel doit laisser l’échéance en statut A_PAYER"""
        Paiement.objects.create(
            echeance=self.echeance,
            montant_paye=10000,
            mode_paiement=Paiement.Mode.ESPECES,
            date_paiement=timezone.now()
        )
        self.assertEqual(self.echeance.reste_a_payer, 20000)
        self.assertEqual(self.echeance.statut, Echeance.Statut.A_PAYER)

    def test_paiement_complet(self):
        """Un paiement complet doit passer l’échéance en statut PAYE"""
        Paiement.objects.create(
            echeance=self.echeance,
            montant_paye=30000,
            mode_paiement=Paiement.Mode.VIREMENT,
            date_paiement=timezone.now()
        )
        # Recharger l’échéance depuis la base
        self.echeance.refresh_from_db()
        self.assertEqual(self.echeance.reste_a_payer, 0)
        self.assertEqual(self.echeance.statut, Echeance.Statut.PAYE)
