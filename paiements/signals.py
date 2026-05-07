import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Paiement, Recu

@receiver(post_save, sender=Paiement)
def generer_recu(sender, instance, created, **kwargs):
    """
    Génère automatiquement un reçu PDF/numéro unique
    lorsqu'un paiement est validé.
    """
    if created and instance.statut == Paiement.Statut.VALIDE:
        numero_unique = f"REC-{uuid.uuid4().hex[:8].upper()}"
        Recu.objects.create(
            paiement=instance,
            numero_recu=numero_unique,
            fichier_url=f"/media/recus/{numero_unique}.pdf",
            signature_comptable="Service Comptable CLEAN"
        )


