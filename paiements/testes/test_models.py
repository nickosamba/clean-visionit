from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from paiements.models import Echeance, Paiement, Recu
from clients.models import Client
from abonnements.models import Abonnement
from secteurs.models import Secteur

User = get_user_model()

class PaiementsModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="comptable",
            email="comptable@example.com",
            password="password",
            role="Comptable"
        )
        self.secteur = Secteur.objects.create(nom="Secteur Test")
        self.abonnement = Abonnement.objects.create(nom="Base", montant_base=100)
        self.client = Client.objects.create(
            prenom="Nicko",
            nom="Test",
            email="nicko@example.com",
            telephone_principal="+111111111",
            abonnement=self.abonnement,
            date_recouvrement=date(2026, 2, 1),  # ✅ champ obligatoire
            statut="Actif",
            montant_mensuel=30000,
        )
        self.echeance = Echeance.objects.create(
            client=self.client,
            montant_du=100,
            date_echeance=date(2026, 2, 1),
            type_echeance=Echeance.Type.MENSUELLE
        )

    # ------------------- Tests Echeance -------------------
    def test_periode_auto_calcul(self):
        self.assertEqual(self.echeance.periode, "2026-01")
        # ✅ accepte anglais ou français selon locale
        self.assertIn(self.echeance.periode_affiche, ["January 2026", "janvier 2026"])

    def test_total_paye_and_reste_a_payer(self):
        Paiement.objects.create(
            echeance=self.echeance,
            utilisateur=self.user,
            montant_paye=40,
            mode_paiement=Paiement.Mode.ESPECES
        )
        Paiement.objects.create(
            echeance=self.echeance,
            utilisateur=self.user,
            montant_paye=60,
            mode_paiement=Paiement.Mode.ESPECES
        )
        self.assertEqual(self.echeance.total_paye, 100)
        self.assertEqual(self.echeance.reste_a_payer, 0)

    # ------------------- Tests Paiement -------------------
    def test_valider_paiement_met_a_jour_echeance(self):
        paiement = Paiement.objects.create(
            echeance=self.echeance,
            utilisateur=self.user,
            montant_paye=100,
            mode_paiement=Paiement.Mode.ESPECES
        )
        paiement.valider()
        self.echeance.refresh_from_db()
        self.assertEqual(self.echeance.statut, Echeance.Statut.PAYE)

    def test_paiement_montant_negatif_interdit(self):
        with self.assertRaises(ValueError):
            Paiement.objects.create(
                echeance=self.echeance,
                utilisateur=self.user,
                montant_paye=-10,
                mode_paiement=Paiement.Mode.ESPECES
            )

    def test_paiement_superieur_montant_attendu_interdit(self):
        with self.assertRaises(ValueError):
            Paiement.objects.create(
                echeance=self.echeance,
                utilisateur=self.user,
                montant_attendu=50,
                montant_paye=60,
                mode_paiement=Paiement.Mode.ESPECES
            )

    # ------------------- Tests Recu -------------------
    def test_recu_creation(self):
        paiement = Paiement.objects.create(
            echeance=self.echeance,
            utilisateur=self.user,
            montant_paye=100,
            mode_paiement=Paiement.Mode.ESPECES
        )
        recu = Recu.objects.create(
            paiement=paiement,
            fichier_url="http://example.com/recu.pdf",
            numero_recu="REC-001"
        )
        self.assertEqual(str(recu), f"Reçu REC-001 - Paiement {paiement.id}")
