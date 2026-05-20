import uuid
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import Paiement, Recu, Echeance

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

@receiver(post_delete, sender=Paiement)
def maj_echeance_apres_suppression_paiement(sender, instance, **kwargs):
    """
    Recalcule le statut de l'échéance après la suppression d'un paiement.
    """
    echeance = instance.echeance
    total_valide = echeance.paiements.filter(
        statut=Paiement.Statut.VALIDE
    ).aggregate(Sum("montant_paye"))["montant_paye__sum"] or 0

    if total_valide >= echeance.montant_du:
        echeance.statut = Echeance.Statut.PAYE
    elif total_valide > 0:
        echeance.statut = Echeance.Statut.A_PAYER
    else:
        echeance.statut = Echeance.Statut.A_PAYER
    
    echeance.save(update_fields=["statut"])


