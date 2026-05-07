# incidents/forms.py
from django import forms
from agents.models import Incident

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

