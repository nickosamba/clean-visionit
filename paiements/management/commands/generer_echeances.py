from django.core.management.base import BaseCommand
from paiements.tasks import generer_echeances_mensuelles

class Command(BaseCommand):
    help = "Génère les échéances mensuelles pour tous les clients actifs"

    def handle(self, *args, **options):
        generer_echeances_mensuelles()
        self.stdout.write(self.style.SUCCESS("Échéances mensuelles générées"))
