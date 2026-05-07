# incidents/forms.py
from django import forms
from .models import Incident, Agent

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ["client", "type_incident", "description", "photo"]  # 👈 ajout du champ client
        widgets = {
            "client": forms.Select(attrs={
                "class": "w-full p-3 border border-slate-200 rounded-xl bg-slate-50 focus:ring-2 focus:ring-amber-500"
            }),
            "type_incident": forms.Select(attrs={
                "class": "w-full p-3 border border-slate-200 rounded-xl bg-slate-50 focus:ring-2 focus:ring-amber-500"
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "class": "w-full p-3 border border-slate-200 rounded-xl bg-slate-50 focus:ring-2 focus:ring-amber-500",
                "placeholder": "Détaillez le problème..."
            }),
            "photo": forms.ClearableFileInput(attrs={
                "class": "w-full p-3 border border-slate-200 rounded-xl bg-slate-50 focus:ring-2 focus:ring-amber-500"
            }),
        }

class AgentPhotoForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ["photo_profile"]
        widgets = {
            "photo_profile": forms.ClearableFileInput(attrs={
                "class": "hidden",  # caché pour styliser avec ton icône caméra
                "accept": "image/*"
            })
        }

from django import forms
from .models import Agent

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        # on inclut tous les champs sauf 'matricule'
        exclude = ["matricule"]

        widgets = {
            "user": forms.Select(attrs={"class": "w-full border rounded px-3 py-2"}),
            "secteur": forms.Select(attrs={"class": "w-full border rounded px-3 py-2"}),
            "zone_intervention": forms.TextInput(attrs={"class": "w-full border rounded px-3 py-2"}),
            "statut": forms.Select(attrs={"class": "w-full border rounded px-3 py-2"}),
            "date_embauche": forms.DateInput(attrs={"class": "w-full border rounded px-3 py-2", "type": "date"}),
            "type_contrat": forms.Select(attrs={"class": "w-full border rounded px-3 py-2"}),
            "telephone_principal": forms.TextInput(attrs={"class": "w-full border rounded px-3 py-2"}),
            "telephone_secondaire": forms.TextInput(attrs={"class": "w-full border rounded px-3 py-2"}),
            "adresse": forms.TextInput(attrs={"class": "w-full border rounded px-3 py-2"}),
            "photo_profile": forms.ClearableFileInput(attrs={"class": "w-full border rounded px-3 py-2"}),
        }

