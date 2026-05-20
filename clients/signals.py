from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta
from datetime import datetime
from clients.models import Client, ClientOption
from paiements.models import Echeance

@receiver(post_save, sender=Client)
def creer_ou_maj_echeances(sender, instance, created, **kwargs):
    """
    Génère la première échéance à la création du client
    ou met à jour le montant des échéances non payées si le client est modifié.
    """
    if instance.date_recouvrement:
        # 🔥 S'assurer que c'est bien un objet date
        premiere = instance.date_recouvrement
        if isinstance(premiere, str):
            premiere = datetime.strptime(premiere, "%Y-%m-%d").date()

        if created:
            periode = (premiere - relativedelta(months=1)).strftime("%Y-%m")
            Echeance.objects.create(
                client=instance,
                montant_du=instance.montant_mensuel,
                periode=periode,
                date_echeance=premiere,
                type_echeance=Echeance.Type.MENSUELLE,
                statut=Echeance.Statut.A_PAYER
            )
        else:
            # Cas de modification : on met à jour uniquement les échéances non réglées
            instance.echeances.filter(
                statut__in=[Echeance.Statut.A_PAYER, Echeance.Statut.EN_RETARD]
            ).update(montant_du=instance.montant_mensuel)


# --- Signal sur ClientOption ---
def maj_montant_et_echeances(client):
    """Recalcule le montant mensuel du client et met à jour les échéances non payées."""
    nouveau_montant = client.calculer_montant_mensuel()
    if client.montant_mensuel != nouveau_montant:
        client.montant_mensuel = nouveau_montant
        client.save(update_fields=["montant_mensuel"])

    client.echeances.filter(
        statut__in=[Echeance.Statut.A_PAYER, Echeance.Statut.EN_RETARD]
    ).update(montant_du=nouveau_montant)


@receiver(post_save, sender=ClientOption)
@receiver(post_delete, sender=ClientOption)
def maj_echeances_apres_option(sender, instance, **kwargs):
    """Déclenché lorsqu'une option est ajoutée, modifiée ou supprimée."""
    maj_montant_et_echeances(instance.client)
