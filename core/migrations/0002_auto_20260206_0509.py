from django.db import migrations
from django.contrib.auth.models import Group

def create_roles(apps, schema_editor):
    roles = ["Agent de terrain", "Comptable", "Gestionnaire", "Administrateur"]
    for role in roles:
        Group.objects.get_or_create(name=role)

class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),  # dépend de ta première migration
    ]

    operations = [
        migrations.RunPython(create_roles),
    ]
