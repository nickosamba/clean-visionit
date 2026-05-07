# paiements/models.py
from django.db import models
from clients.models import Client
from accounts.models import User
from django.db.models import Sum
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from agents.models import *

class Echeance(models.Model):

    class Type(models.TextChoices):
        MENSUELLE = "Mensuelle", "Mensuelle"
        ANNUELLE = "Annuelle", "Annuelle"
        EXCEPTIONNELLE = "Exceptionnelle", "Exceptionnelle"

    class Statut(models.TextChoices):
        A_PAYER = "A payer", "A payer"
        PAYE = "Payé", "Payé"
        EN_RETARD = "En retard", "En retard"

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="echeances")
    montant_du = models.DecimalField(max_digits=10, decimal_places=2)
    periode = models.CharField(max_length=7, blank=True)  # ex: "2025-01"
    date_echeance = models.DateField(null=True, blank=True) # ✅ date exacte du recouvrement
    type_echeance = models.CharField(max_length=20, choices=Type.choices)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.A_PAYER)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # ⚡ Calcul automatique de la période si non renseignée
        if self.date_echeance and not self.periode:
            mois_consomme = self.date_echeance - relativedelta(months=1)
            self.periode = mois_consomme.strftime("%Y-%m")
        super().save(*args, **kwargs)

    @property
    def periode_affiche(self):
        mois_consomme = self.date_echeance - relativedelta(months=1)
        return mois_consomme.strftime("%B %Y").capitalize()


    @property 
    def total_paye(self): 
        """Somme des paiements déjà effectués pour cette échéance.""" 
        return self.paiements.aggregate(Sum("montant_paye"))["montant_paye__sum"] or 0 
    @property 
    def reste_a_payer(self): 
        """Montant restant à payer.""" 
        return max(self.montant_du - self.total_paye, 0)

    def __str__(self):
        return f"{self.client} - {self.periode} ({self.statut})"

class Paiement(models.Model):

    class Mode(models.TextChoices):
        ESPECES = "Espèces", "Espèces"
        MOBILE_MONEY = "Mobile Money", "Mobile Money"
        VIREMENT = "Virement", "Virement"

    class Statut(models.TextChoices):
        VALIDE = "Validé", "Validé"
        ANNULE = "Annulé", "Annulé"
        ERREUR = "Erreur", "Erreur"

    echeance = models.ForeignKey(Echeance, on_delete=models.CASCADE, related_name="paiements")
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    montant_attendu = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2)

    date_paiement = models.DateTimeField(default=timezone.now)
    mode_paiement = models.CharField(max_length=20, choices=Mode.choices)
    reference_transaction = models.CharField(max_length=100, blank=True, null=True, unique=True)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.VALIDE)
    notes = models.TextField(blank=True, null=True, help_text="Commentaires ou référence interne")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # ✅ audit complet

    class Meta:
        indexes = [
            models.Index(fields=["date_paiement"]),
            models.Index(fields=["mode_paiement"]),
            models.Index(fields=["statut"]),
        ]

    def __str__(self):
        return f"Paiement {self.id} - {self.montant_paye} FCFA ({self.mode_paiement})"

    # def valider(self):
    #     """Valide le paiement et met à jour l’échéance associée."""
    #     self.statut = Paiement.Statut.VALIDE
    #     self.echeance.statut = Echeance.Statut.PAYE
    #     self.echeance.save()
    #     self.save()
    
    def valider(self): 
        """Valide le paiement et met à jour l’échéance associée avec atomicité.""" 
        from django.db import transaction
        with transaction.atomic():
            self.statut = Paiement.Statut.VALIDE 
            self.save() 
            # Le statut de l'échéance est mis à jour dans la méthode save()

    def save(self, *args, **kwargs):
        from django.db import transaction
        
        if self.montant_paye <= 0:
            raise ValueError("Le montant payé doit être positif.")

        # Vérification par rapport au montant attendu (si défini)
        if self.montant_attendu and self.montant_paye > self.montant_attendu:
             raise ValueError("Le montant payé ne peut pas dépasser le montant attendu.")
        
        # Vérification du surpaiement (en ignorant le paiement actuel s'il existe déjà)
        total_autres = self.echeance.paiements.filter(
            statut=Paiement.Statut.VALIDE
        ).exclude(id=self.id).aggregate(Sum("montant_paye"))["montant_paye__sum"] or 0
        
        if total_autres + self.montant_paye > self.echeance.montant_du:
            if self.statut == Paiement.Statut.VALIDE:
                raise ValueError(f"Ce paiement dépasse le montant dû. Reste à payer : {self.echeance.montant_du - total_autres} FCFA")

        with transaction.atomic():
            super().save(*args, **kwargs)

            # Recalcul systématique du statut de l'échéance
            total_valide = self.echeance.paiements.filter(
                statut=Paiement.Statut.VALIDE
            ).aggregate(Sum("montant_paye"))["montant_paye__sum"] or 0

            if total_valide >= self.echeance.montant_du:
                self.echeance.statut = Echeance.Statut.PAYE
            elif total_valide > 0:
                self.echeance.statut = Echeance.Statut.A_PAYER # Ou un statut "Partiellement payé" si vous en ajoutez un
            else:
                self.echeance.statut = Echeance.Statut.A_PAYER
            
            self.echeance.save(update_fields=["statut"])


class Recu(models.Model):
    paiement = models.ForeignKey(Paiement, on_delete=models.CASCADE, related_name="recus", null=True, blank=True)
    fichier_url = models.URLField(max_length=200) # sécurité renforcée
    numero_recu = models.CharField(max_length=50, unique=True, blank=True, null=True)
    signature_comptable = models.CharField(max_length=100, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # audit complet

    def __str__(self):
        return f"Reçu {self.numero_recu} - Paiement {self.paiement.id}"







class Salaire(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="salaires")
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    periode = models.DateField() # ✅ ex: 2026-02-01
    date_versement = models.DateField(null=True, blank=True) # ✅ optionnel
    statut = models.CharField(
        max_length=20,
        choices=[("Prévu", "Prévu"), ("Payé", "Payé"), ("En retard", "En retard")],
        default="Prévu"
    )
    prime = models.DecimalField(max_digits=10, decimal_places=2, default=0) # ✅ ajouté
    # def __str__(self):
    #     return f"Salaire {self.agent} - {self.periode} ({self.statut})"

    @property 
    def periode_affiche(self): 
        return self.periode.strftime("%B %Y") 
    # ex: "Février 2026" 
    def __str__(self): 
        return f"{self.agent} - {self.periode_affiche} ({self.statut})"

