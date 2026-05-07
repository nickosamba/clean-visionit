# agents/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from agents.models import Agent

@receiver(post_save, sender=User)
def create_agent_profile(sender, instance, created, **kwargs):
    # Create an agent profile when a user with "Agent de terrain" role is newly created
    if created and hasattr(instance, 'role') and instance.role == "Agent de terrain":
        Agent.objects.create(
            user=instance,
            telephone_principal="0000000000",  # Default phone number to satisfy not-null constraint
            statut="Actif",  # Default status
            type_contrat="CDI"  # Default contract type
        )


# @receiver(post_save, sender=Agent)
# def generate_matricule(sender, instance, created, **kwargs):
#     if created and not instance.matricule:
#         instance.matricule = f"AGT-{instance.id}"
#         instance.save(update_fields=["matricule"])
