# tournees/models.py
from django.db import models
from secteurs.models import Secteur
from agents.models import Agent
from clients.models import Client

class Tournee(models.Model):

    class Statut(models.TextChoices):
        PLANIFIE = "Planifié", "Planifié"
        EN_COURS = "En cours", "En cours"
        TERMINE = "Terminé", "Terminé"
        ANNULE = "Annulé", "Annulé"

    date = models.DateField()
    date_planification = models.DateField(auto_now_add=True)

    secteur = models.ForeignKey(Secteur, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.PLANIFIE)
    heure_debut = models.TimeField(blank=True, null=True)
    heure_fin = models.TimeField(blank=True, null=True)
    vehicule = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tournée {self.id} - {self.agent.user.email} - {self.date}"


class TourneeClient(models.Model):

    class StatutService(models.TextChoices):
        PLANIFIE = "Planifié", "Planifié"
        SERVI = "Servi", "Servi"
        ABSENT = "Absent", "Absent"
        PROBLEME = "Problème signalé", "Problème signalé"

    tournee = models.ForeignKey(Tournee, on_delete=models.CASCADE, related_name="clients")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    heure_passage = models.DateTimeField(blank=True, null=True)
    statut_service = models.CharField(max_length=30, choices=StatutService.choices, default=StatutService.PLANIFIE)
    commentaires_agent = models.TextField(blank=True, null=True)
    photo_preuve = models.TextField(blank=True, null=True)
    signature_client = models.TextField(blank=True, null=True)
    photo_preuve = models.ImageField(upload_to="preuves_tournees/", blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TournéeClient {self.id} - Tournée {self.tournee.id} - Client {self.client.code_client}"