from django import forms
from .models import Secteur, Rue

class SecteurForm(forms.ModelForm):
    class Meta:
        model = Secteur
        fields = ["nom", "ville", "pays", "description"]
        
        base_input = "w-full px-4 py-3 rounded-xl border-slate-200 bg-slate-50 focus:bg-white focus:border-emerald-500 focus:ring-emerald-500 transition-all"
        
        widgets = {
            "nom": forms.TextInput(attrs={
                "class": base_input,
                "placeholder": "Ex: Makélékélé, Poto-Poto..."
            }),
            "ville": forms.TextInput(attrs={
                "class": base_input,
            }),
            "pays": forms.TextInput(attrs={
                "class": base_input,
            }),
            "description": forms.Textarea(attrs={
                "class": base_input,
                "rows": 3,
                "placeholder": "Informations complémentaires sur la zone..."
            }),
        }

class RueForm(forms.ModelForm):
    class Meta:
        model = Rue
        fields = ["nom", "type_voie", "secteur", "gps_lat", "gps_lon"]
        
        base_input = "w-full px-4 py-3 rounded-xl border-slate-200 bg-slate-50 focus:bg-white focus:border-emerald-500 focus:ring-emerald-500 transition-all"
        
        widgets = {
            "nom": forms.TextInput(attrs={
                "class": base_input,
                "placeholder": "Ex: Avenue de l'Indépendance"
            }),
            "type_voie": forms.Select(attrs={
                "class": base_input,
            }),
            "secteur": forms.Select(attrs={
                "class": base_input,
            }),
            "gps_lat": forms.NumberInput(attrs={
                "class": base_input,
                "placeholder": "-4.26..."
            }),
            "gps_lon": forms.NumberInput(attrs={
                "class": base_input,
                "placeholder": "15.24..."
            }),
        }
