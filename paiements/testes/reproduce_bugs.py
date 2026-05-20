from django.test import TestCase, Client as HttpClient
from django.contrib.auth import get_user_model
from datetime import date
from paiements.models import Echeance, Paiement, Recu
from clients.models import Client
from abonnements.models import Abonnement
from secteurs.models import Secteur, Rue
from django.urls import reverse

User = get_user_model()

class BugReproductionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="comptable",
            email="comptable@example.com",
            password="password",
            role="Comptable"
        )
        self.secteur = Secteur.objects.create(nom="Secteur Test")
        self.rue = Rue.objects.create(nom="Rue Test", secteur=self.secteur)
        self.abonnement = Abonnement.objects.create(nom="Base", montant_base=10000)
        self.client_obj = Client.objects.create(
            prenom="Test",
            nom="Client",
            email="test@example.com",
            telephone_principal="+123456789",
            abonnement=self.abonnement,
            rue=self.rue,
            date_recouvrement=date(2026, 2, 1),
            statut="Actif",
        )
        # L'échéance est normalement créée par le signal creer_ou_maj_echeances
        self.echeance = self.client_obj.echeances.first()

    def test_duplicate_receipt_creation(self):
        """Vérifie si deux reçus sont créés lors d'un paiement via la vue payer_echeance."""
        self.client.login(email="comptable@example.com", password="password")
        url = reverse("dashboard:payer_echeance", kwargs={"echeance_id": self.echeance.id})
        
        # On simule un paiement
        response = self.client.post(url, {
            "montant_paye": 5000,
            "mode_paiement": "Espèces"
        })
        
        self.assertEqual(response.status_code, 302) # Redirection après succès
        
        # Vérification du nombre de paiements
        paiements = Paiement.objects.filter(echeance=self.echeance)
        self.assertEqual(paiements.count(), 1)
        
        # Vérification du nombre de reçus
        recus = Recu.objects.filter(paiement=paiements[0])
        self.assertEqual(recus.count(), 1, f"Attendu 1 reçu, trouvé {recus.count()}")

    def test_client_save_recursion_and_redundancy(self):
        """Vérifie si la sauvegarde d'un client déclenche plusieurs saves inutiles."""
        # On va compter les appels au signal post_save
        from django.db.models.signals import post_save
        from unittest.mock import MagicMock
        
        handler = MagicMock()
        post_save.connect(handler, sender=Client)
        
        self.client_obj.nom = "Updated Name"
        self.client_obj.save()
        
        # On s'attend à ce que post_save soit appelé une seule fois (ou deux si montant_mensuel change)
        # Mais ici on vérifie surtout s'il n'y a pas de boucle infinie ou d'appels excessifs
        print(f"DEBUG: post_save called {handler.call_count} times")
        # Si c'est appelé plus de 2-3 fois, il y a un problème de redondance
        self.assertLessEqual(handler.call_count, 3) 
        
        post_save.disconnect(handler, sender=Client)
