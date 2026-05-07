# abonnements/models.py
from django.db import models

class Abonnement(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    montant_base = models.DecimalField(max_digits=10, decimal_places=2)
    avantages = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class TarifHistorique(models.Model):
    abonnement = models.ForeignKey(Abonnement, on_delete=models.CASCADE, related_name="historique")
    ancien_montant = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    nouveau_montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_changement = models.DateField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.abonnement.nom} ({self.date_changement})"


class OptionService(models.Model):

    class Statut(models.TextChoices):
        ACTIVE = "Active", "Active"
        INACTIVE = "Inactive", "Inactive"

    nom = models.CharField(max_length=100)
    prix_supplementaire = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    abonnement = models.ForeignKey(
    Abonnement,
    on_delete=models.CASCADE,
    related_name="options",
    null=True,
    blank=True
)


    def __str__(self):
        return self.nom
