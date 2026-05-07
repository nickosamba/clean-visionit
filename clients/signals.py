from django.db.models.signals import post_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta
from clients.models import Client
from paiements.models import Echeance 
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta
from clients.models import Client, ClientOption
from paiements.models import Echeance

from datetime import datetime

#@receiver(post_save, sender=Client)
@receiver(post_save, sender=Client)
def creer_ou_maj_echeances(sender, instance, created, **kwargs):
    # ⚡ Toujours recalculer le montant mensuel
    montant = instance.calculer_montant_mensuel()
    if instance.montant_mensuel != montant:
        instance.montant_mensuel = montant
        instance.save(update_fields=["montant_mensuel"])

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
            instance.echeances.filter(
                statut__in=[Echeance.Statut.A_PAYER, Echeance.Statut.EN_RETARD]
            ).update(montant_du=instance.montant_mensuel)

# def creer_ou_maj_echeances(sender, instance, created, **kwargs):
#     # ⚡ Toujours recalculer le montant mensuel
#     montant = instance.calculer_montant_mensuel()
#     if instance.montant_mensuel != montant:
#         instance.montant_mensuel = montant
#         instance.save(update_fields=["montant_mensuel"])

#     # Cas 1 : Création du client → générer uniquement la première échéance
#     if created and instance.date_recouvrement:
#         premiere = instance.date_recouvrement
#         periode = (premiere - relativedelta(months=1)).strftime("%Y-%m")

#         Echeance.objects.create(
#             client=instance,
#             montant_du=instance.montant_mensuel,
#             periode=periode,
#             date_echeance=premiere,
#             type_echeance=Echeance.Type.MENSUELLE,
#             statut=Echeance.Statut.A_PAYER
#         )

#     # Cas 2 : Modification du client → mettre à jour les échéances non payées
#     else:
#         instance.echeances.filter(
#             statut__in=[Echeance.Statut.A_PAYER, Echeance.Statut.EN_RETARD]
#         ).update(montant_du=instance.montant_mensuel)


# --- Signal sur ClientOption ---
def maj_montant_et_echeances(client):
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
    maj_montant_et_echeances(instance.client)

