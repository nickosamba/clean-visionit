from django import forms
from .models import OptionService

class OptionServiceForm(forms.ModelForm):
    class Meta:
        model = OptionService
        fields = ["nom", "prix_supplementaire", "description", "statut"]
        widgets = {
            "nom": forms.TextInput(attrs={
                "class": "w-full p-2 border rounded-lg focus:ring-2 focus:ring-emerald-500",
                "placeholder": "Nom de l'option"
            }),
            "prix_supplementaire": forms.NumberInput(attrs={
                "class": "w-full p-2 border rounded-lg focus:ring-2 focus:ring-emerald-500",
                "placeholder": "Prix supplémentaire"
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full p-2 border rounded-lg focus:ring-2 focus:ring-emerald-500",
                "rows": 3,
                "placeholder": "Description de l'option"
            }),
            "statut": forms.Select(attrs={
                "class": "w-full p-2 border rounded-lg focus:ring-2 focus:ring-emerald-500"
            }),
        }
