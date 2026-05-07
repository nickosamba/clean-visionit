# secteurs/models.py
from django.db import models
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

class Secteur(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.CharField(max_length=100, default="Brazzaville") 
    pays = models.CharField(max_length=100, default="Congo")
    code = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last_id = Secteur.objects.order_by("id").last()
            next_number = 1 if not last_id else last_id.id + 1
            self.code = f"SEC-{next_number:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

# from django.db import models
# from geopy.geocoders import Nominatim

class Rue(models.Model):

    class TypeVoie(models.TextChoices):
        RUE = "Rue", "Rue"
        AVENUE = "Avenue", "Avenue"
        BOULEVARD = "Boulevard", "Boulevard"
        ALLEE = "Allée", "Allée"

    nom = models.CharField(max_length=150)
    secteur = models.ForeignKey("Secteur", on_delete=models.CASCADE, related_name="rues")
    type_voie = models.CharField(max_length=20, choices=TypeVoie.choices, blank=True, null=True)
    gps_lat = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    gps_lon = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last_id = Rue.objects.order_by("id").last()
            next_number = 1 if not last_id else last_id.id + 1
            self.code = f"RUE-{next_number:03d}"

        if not self.gps_lat or not self.gps_lon:
            try:
                geolocator = Nominatim(user_agent="clean_geocoder", timeout=5)
                query = f"{self.type_voie or ''} {self.nom}, {self.secteur.nom}, {self.secteur.ville}, {self.secteur.pays}"
                location = geolocator.geocode(query)

                if location:
                    self.gps_lat = round(float(location.latitude), 6)
                    self.gps_lon = round(float(location.longitude), 6)
                else:
                    # fallback : juste ville + pays
                    fallback = geolocator.geocode(f"{self.secteur.ville}, {self.secteur.pays}")
                    if fallback:
                        self.gps_lat = round(float(fallback.latitude), 6)
                        self.gps_lon = round(float(fallback.longitude), 6)

            except (GeocoderTimedOut, GeocoderServiceError):
                # On ignore l’erreur → la rue est quand même créée
                pass

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code or ''} - {self.type_voie or ''} {self.nom}".strip()



