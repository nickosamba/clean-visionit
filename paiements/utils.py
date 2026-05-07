from django.utils import timezone
from paiements.models import Echeance

def creer_echeance_auto(client, montant, type_echeance="Mensuelle", periode=None):
    """
    Crée automatiquement une échéance pour un client.
    
    :param client: instance du modèle Client
    :param montant: montant dû (Decimal ou float)
    :param type_echeance: type d’échéance ("Mensuelle", "Annuelle", "Exceptionnelle")
    :param periode: période au format "YYYY-MM" (par défaut mois courant)
    :return: instance Echeance créée
    """
    if periode is None:
        periode = timezone.now().strftime("%Y-%m")  # ex: "2026-01"

    echeance = Echeance.objects.create(
        client=client,
        montant_du=montant,
        periode=periode,
        type_echeance=type_echeance,
        statut=Echeance.Statut.A_PAYER
    )
    return echeance
