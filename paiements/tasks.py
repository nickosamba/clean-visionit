from django.utils.timezone import now
from clients.models import Client
from paiements.models import Echeance
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

def generer_echeances_mensuelles():
    """
    Génère les échéances pour tous les clients actifs pour le mois en cours.
    Sécurisé par une transaction atomique.
    """
    today = now().date()
    periode = today.strftime("%Y-%m")
    count = 0

    with transaction.atomic():
        clients_actifs = Client.objects.filter(statut=Client.Statut.ACTIF)
        
        for client in clients_actifs:
            # Vérifier si l'échéance existe déjà pour éviter les doublons
            if not Echeance.objects.filter(client=client, periode=periode).exists():
                try:
                    Echeance.objects.create(
                        client=client,
                        montant_du=client.montant_mensuel,
                        periode=periode,
                        date_echeance=today,
                        type_echeance=Echeance.Type.MENSUELLE,
                        statut=Echeance.Statut.A_PAYER
                    )
                    count += 1
                except Exception as e:
                    logger.error(f"Erreur lors de la création de l'échéance pour le client {client.id}: {e}")

    return f"{count} échéances générées pour la période {periode}."
