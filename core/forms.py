from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'role', 'deux_facteurs_active']

        widgets = {
            'username': forms.TextInput(attrs={
                "class": "form-input h-14 w-full rounded-lg border p-3.5"
            }),
            'email': forms.EmailInput(attrs={
                "class": "form-input h-14 w-full rounded-lg border p-3.5"
            }),
            'role': forms.Select(attrs={
                "class": "form-select h-14 w-full rounded-lg border p-3.5"
            }),
            'deux_facteurs_active': forms.CheckboxInput(),
        }


class UserPasswordForm(forms.Form):
    password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={
            "class": "form-input h-14 w-full rounded-lg border p-3.5"
        })
    )
    password2 = forms.CharField(
        label="Confirmez le mot de passe",
        widget=forms.PasswordInput(attrs={
            "class": "form-input h-14 w-full rounded-lg border p-3.5"
        })
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned


from django import forms
from django.shortcuts import render, redirect
from paiements.models import Salaire
from agents.models import Agent
from django.contrib.auth.decorators import login_required
from core.decorators import role_required

# class SalaireForm(forms.ModelForm):
#     class Meta:
#         model = Salaire
#         fields = ["agent", "periode", "montant", "prime", "statut"]


from django import forms
from paiements.models import Salaire

class SalaireForm(forms.ModelForm):
    class Meta:
        model = Salaire
        fields = ["agent", "montant", "periode", "statut", "date_versement"]
        widgets = {
            "periode": forms.TextInput(attrs={"placeholder": "ex: Janvier 2026"}),
            "montant": forms.NumberInput(attrs={"class": "form-control"}),
            "date_versement": forms.DateInput(attrs={"type": "date"}),
        }
