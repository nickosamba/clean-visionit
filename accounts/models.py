# utilisateurs/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = [
        ("Administrateur", "Administrateur"),
        ("Gestionnaire", "Gestionnaire"),
        ("Agent de terrain", "Agent de terrain"),
        ("Comptable", "Comptable"),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    deux_facteurs_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email} ({self.role})"


class AuditLog(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=200)
    entite = models.CharField(max_length=100)
    entite_id = models.IntegerField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    device_info = models.CharField(max_length=100, blank=True, null=True)
    date_action = models.DateTimeField(auto_now_add=True)
