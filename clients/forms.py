# from django import forms
# from .models import Client, OptionService

# class ClientForm(forms.ModelForm):
#     options = forms.ModelMultipleChoiceField( queryset=OptionService.objects.all(), required=False, widget=forms.SelectMultiple(attrs={ "class": "w-full px-4 py-2 border border-slate-300 rounded-lg", "id": "id_options" }) )
#     class Meta:
#         model = Client
#         fields = [
#             "prenom",
#             "nom",
#             "email",
#             "telephone_principal",
#             "telephone_secondaire",
#             "adresse_numero",
#             "rue",
#             "abonnement",
#             "date_debut",
#             "date_recouvrement",
#             "statut",
#             "commentaires",
#             "gps_lat",
#             "gps_lon",
#             "options", 
#         ]

#         base_input = "w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"

#         widgets = {
#             "prenom": forms.TextInput(attrs={"class": base_input}),
#             "nom": forms.TextInput(attrs={"class": base_input}),
#             "email": forms.EmailInput(attrs={"class": base_input}),
#             "telephone_principal": forms.TextInput(attrs={"class": base_input}),
#             "telephone_secondaire": forms.TextInput(attrs={"class": base_input}),
#             "adresse_numero": forms.TextInput(attrs={"class": base_input}),
#             "rue": forms.Select(attrs={"class": base_input}),
#             "abonnement": forms.Select(attrs={"class": base_input}),

#             # 🔥 LIGNE CORRECTE
#             "date_debut": forms.DateInput(
#                 attrs={"class": base_input, "type": "date"},
#                 format="%Y-%m-%d"
#             ),

#             "date_recouvrement": forms.DateInput(
#                 attrs={
#                     "class": base_input,
#                     "type": "date",  # ✅ HTML5 calendrier
#                 },
#                 format="%Y-%m-%d"   # ✅ format attendu
#             ),


#             "statut": forms.Select(attrs={"class": base_input}),
#             "commentaires": forms.Textarea(attrs={"class": base_input}),
#             "gps_lat": forms.NumberInput(attrs={"class": base_input}),
#             "gps_lon": forms.NumberInput(attrs={"class": base_input}),
#         }

#     # 🔥 OBLIGATOIRE pour que Django accepte le format HTML5
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["date_debut"].input_formats = ["%Y-%m-%d"]
#         self.fields["date_recouvrement"].input_formats = ["%Y-%m-%d"]

from django import forms
from .models import Client, ClientOption, OptionService

class ClientForm(forms.ModelForm):
    options = forms.ModelMultipleChoiceField(
        queryset=OptionService.objects.all(),
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                "class": "w-full px-4 py-2 border border-slate-300 rounded-lg",
                "id": "id_options"
            }
        )
    )

    class Meta:
        model = Client
        fields = [
            "prenom",
            "nom",
            "email",
            "telephone_principal",
            "telephone_secondaire",
            "adresse_numero",
            "rue",
            "abonnement",
            "date_debut",
            "date_recouvrement",
            "statut",
            "commentaires",
            "gps_lat",
            "gps_lon",
            "options",
        ]

        base_input = "w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"

        widgets = {
            "prenom": forms.TextInput(attrs={"class": base_input}),
            "nom": forms.TextInput(attrs={"class": base_input}),
            "email": forms.EmailInput(attrs={"class": base_input}),
            "telephone_principal": forms.TextInput(attrs={"class": base_input}),
            "telephone_secondaire": forms.TextInput(attrs={"class": base_input}),
            "adresse_numero": forms.TextInput(attrs={"class": base_input}),
            "rue": forms.Select(attrs={"class": base_input}),
            "abonnement": forms.Select(attrs={"class": base_input}),
            "date_debut": forms.DateInput(attrs={"class": base_input, "type": "date"}, format="%Y-%m-%d"),
            "date_recouvrement": forms.DateInput(attrs={"class": base_input, "type": "date"}, format="%Y-%m-%d"),
            "statut": forms.Select(attrs={"class": base_input}),
            "commentaires": forms.Textarea(attrs={"class": base_input}),
            "gps_lat": forms.NumberInput(attrs={"class": base_input}),
            "gps_lon": forms.NumberInput(attrs={"class": base_input}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_debut"].input_formats = ["%Y-%m-%d"]
        self.fields["date_recouvrement"].input_formats = ["%Y-%m-%d"]

    def save(self, commit=True):
        client = super().save(commit=commit)

        if commit:
            # 🔥 Supprimer les anciennes options
            ClientOption.objects.filter(client=client).delete()

            # 🔥 Ajouter les nouvelles options
            for option in self.cleaned_data.get("options", []):
                ClientOption.objects.create(client=client, option=option)

            # 🔥 Recalculer le montant mensuel
            client.montant_mensuel = client.calculer_montant_mensuel()
            client.save(update_fields=["montant_mensuel"])

        return client
