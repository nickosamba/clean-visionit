# clients/models.py
from django.db import models
from secteurs.models import Rue
from abonnements.models import Abonnement, OptionService
from django.core.validators import RegexValidator, EmailValidator
from django.core.validators import MinValueValidator, MaxValueValidator

class Client(models.Model):

    class Statut(models.TextChoices):
        ACTIF = "Actif", "Actif"
        SUSPENDU = "Suspendu", "Suspendu"
        RESILIE = "Résilié", "Résilié"

    code_client = models.CharField(max_length=50, unique=True, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    nom = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True, validators=[EmailValidator(message="Veuillez entrer un email valide")])
    telephone_principal = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+?\d{9,15}$', message="Numéro de téléphone invalide")])
    telephone_secondaire = models.CharField(max_length=20, blank=True, null=True, validators=[RegexValidator(regex=r'^\+?\d{9,15}$', message="Numéro de téléphone invalide")])
    adresse_numero = models.CharField(max_length=50, blank=True, null=True)

    rue = models.ForeignKey(Rue, on_delete=models.SET_NULL, null=True, related_name="clients")
    abonnement = models.ForeignKey(Abonnement, on_delete=models.SET_NULL, null=True, related_name="clients")
    montant_mensuel = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    date_debut = models.DateField(blank=True, null=True)
    date_recouvrement = models.DateField(help_text="Date exacte du premier recouvrement")
    
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.ACTIF)
    commentaires = models.TextField(blank=True, null=True)

    gps_lat = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    gps_lon = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["nom", "prenom"]
        indexes = [
            models.Index(fields=["code_client"]),
            models.Index(fields=["statut"]),
            models.Index(fields=["rue"]),
            models.Index(fields=["abonnement"]),
        ]

    def __str__(self):
        return f"{self.nom} {self.prenom or ''}".strip()

    def full_name(self):
        """Retourne le nom complet du client."""
        return f"{self.prenom or ''} {self.nom}".strip()

    

    def calculer_montant_mensuel(self):
        base = self.abonnement.montant_base if self.abonnement else 0
        options_total = sum(opt.option.prix_supplementaire for opt in self.options.all())
        return base + options_total

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        # 1. Pré-remplissage des coordonnées GPS depuis la rue si absentes
        if self.rue and (self.gps_lat is None or self.gps_lon is None):
            self.gps_lat = self.rue.gps_lat
            self.gps_lon = self.rue.gps_lon

        # 2. Sauvegarde initiale
        super().save(*args, **kwargs)

        # 3. Traitements post-sauvegarde nécessitant un ID
        update_needed = False
        update_fields = []

        if is_new and not self.code_client:
            base = (self.nom[:8]).upper()
            self.code_client = f"{base}-{self.id}"
            update_fields.append("code_client")
            update_needed = True

        # Le montant mensuel peut dépendre des options (ClientOption) 
        # qui ne sont pas forcément présentes à la création,
        # mais on fait un calcul initial ici si nécessaire.
        nouveau_montant = self.calculer_montant_mensuel()
        if self.montant_mensuel != nouveau_montant:
            self.montant_mensuel = nouveau_montant
            update_fields.append("montant_mensuel")
            update_needed = True

        if update_needed:
            super().save(update_fields=update_fields)


class ClientOption(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="options")
    option = models.ForeignKey(OptionService, on_delete=models.CASCADE)
    valeur = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client} - {self.option.nom} : {self.valeur or 'N/A'}"