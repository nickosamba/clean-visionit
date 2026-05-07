from django.db.models.signals import post_save
from django.dispatch import receiver
from abonnements.models import OptionService
from clients.models import Client

@receiver(post_save, sender=OptionService)
def update_clients_montant(sender, instance, **kwargs):
    # 🔥 Recalculer les montants des clients liés à cette option
    for client_option in instance.clientoption_set.all():
        client = client_option.client
        client.montant_mensuel = client.calculer_montant_mensuel()
        client.save(update_fields=["montant_mensuel"])
