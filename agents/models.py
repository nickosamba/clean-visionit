# agents/models.py
from django.db import models
from accounts.models import User
from secteurs.models import Secteur
from django.utils import timezone
class Agent(models.Model):

    class Statut(models.TextChoices):
        ACTIF = "Actif", "Actif"
        INACTIF = "Inactif", "Inactif"
        SUSPENDU = "Suspendu", "Suspendu"
        EN_CONGE = "En congé", "En congé"

    class Contrat(models.TextChoices):
        CDI = "CDI", "CDI"
        CDD = "CDD", "CDD"
        PRESTATAIRE = "Prestataire", "Prestataire"
        STAGIAIRE = "Stagiaire", "Stagiaire"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="agent")
    secteur = models.ForeignKey(Secteur, on_delete=models.CASCADE, null=True, blank=True)
    matricule = models.CharField(max_length=50)
    zone_intervention = models.CharField(max_length=150, blank=True, null=True)

    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.ACTIF)
    date_embauche = models.DateField(blank=True, null=True)
    type_contrat = models.CharField(max_length=20, choices=Contrat.choices)
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    telephone_principal = models.CharField(max_length=20)
    telephone_secondaire = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    photo_profile = models.ImageField(upload_to="profile/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # def save(self, *args, **kwargs): 
    #     if not self.matricule: 
    #         base = "AGT" 
    #         self.matricule = f"{base}-{self.id or ''}" 
    #         super().save(*args, **kwargs)


 
    def save(self, *args, **kwargs):
        creating = self.pk is None  # True si l'agent n'existe pas encore

        super().save(*args, **kwargs)  # Sauvegarde normale

        # Génération du matricule uniquement à la création
        if creating and not self.matricule:
            year = timezone.now().year
            self.matricule = f"AGT-{year}-{self.id:04d}"
            super().save(update_fields=["matricule"])

    def __str__(self):
        return f"{self.user.email} ({self.matricule})"

from django.db import models
from accounts.models import User
from clients.models import Client

class Incident(models.Model):
    TYPES = [
        ("Client absent", "Client absent"),
        ("Accès bloqué", "Accès bloqué"),
        ("Panne camion", "Panne camion"),
        ("Bac endommagé", "Bac endommagé"),
        ("Autre", "Autre"),
    ]

    class StatutIncident(models.TextChoices):
        OUVERT = "Ouvert", "Ouvert"
        EN_COURS = "En cours", "En cours"
        RESOLU = "Résolu", "Résolu"
        IGNORE = "Ignoré", "Ignoré"

    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="incidents")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    type_incident = models.CharField(max_length=50, choices=TYPES)
    description = models.TextField(blank=True, null=True)
    
    statut = models.CharField(max_length=20, choices=StatutIncident.choices, default=StatutIncident.OUVERT)
    notes_gestionnaire = models.TextField(blank=True, null=True)
    
    photo = models.ImageField(upload_to="incidents/", blank=True, null=True)
    date_signalement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_incident} - {self.agent.email}"
