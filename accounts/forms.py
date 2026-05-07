from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email *",  # Label displayed to users
        widget=forms.EmailInput(  # Email input widget with custom styling
            attrs={
                "class": "form-input h-14 w-full min-w-0 flex-1 resize-none overflow-hidden "
                         "rounded-lg border border-border-light bg-background-light p-3.5 pl-12 "
                         "text-base font-normal leading-normal text-text-light "
                         "placeholder:text-text-secondary-light focus:border-primary focus:outline-0 "
                         "focus:ring-2 focus:ring-primary/20 dark:border-border-dark "
                         "dark:bg-background-dark dark:text-text-dark "
                         "dark:placeholder:text-text-secondary-dark dark:focus:border-primary",
                "placeholder": "exemple@domaine.com",  # Placeholder text for the input
            }
        )
    )
    password = forms.CharField(
        label="Mot de passe *",  # Label displayed to users
        widget=forms.PasswordInput(  # Password input widget with custom styling
            attrs={
                "class": "form-input h-14 w-full min-w-0 flex-1 resize-none overflow-hidden "
                         "rounded-lg border border-border-light bg-background-light p-3.5 pl-12 "
                         "text-base font-normal leading-normal text-text-light "
                         "placeholder:text-text-secondary-light focus:border-primary focus:outline-0 "
                         "focus:ring-2 focus:ring-primary/20 dark:border-border-dark "
                         "dark:bg-background-dark dark:text-text-dark "
                         "dark:placeholder:text-text-secondary-dark dark:focus:border-primary",
                "placeholder": "Entrez votre mot de passe",  # Placeholder text for the input
            }
        )
    )


class RegisterForm(forms.ModelForm):
    role = forms.ChoiceField(
        label="Rôle *",  # Label displayed to users
        choices=User.ROLE_CHOICES,  # Use role choices defined in User model
        widget=forms.Select(  # Dropdown widget with custom styling
            attrs={
                "class": "form-select h-14 w-full min-w-0 flex-1 resize-none overflow-hidden "
                         "rounded-lg border border-border-light bg-background-light p-3.5 pl-12 "
                         "text-base font-normal leading-normal text-text-light "
                         "placeholder:text-text-secondary-light focus:border-primary focus:outline-0 "
                         "focus:ring-2 focus:ring-primary/20 dark:border-border-dark "
                         "dark:bg-background-dark dark:text-text-dark "
                         "dark:placeholder:text-text-secondary-dark dark:focus:border-primary"
            }
        )
    )

    password1 = forms.CharField(
        label="Mot de passe *",  # Label displayed to users
        strip=False,  # Don't strip whitespace from password
        widget=forms.PasswordInput(attrs={  # Password input widget with custom styling
            "class": "form-input h-14 w-full min-w-0 flex-1 resize-none overflow-hidden "
                     "rounded-lg border border-border-light bg-background-light p-3.5 pl-12 "
                     "text-base font-normal leading-normal text-text-light "
                     "placeholder:text-text-secondary-light focus:border-primary focus:outline-0 "
                     "focus:ring-2 focus:ring-primary/20 dark:border-border-dark "
                     "dark:bg-background-dark dark:text-text-dark "
                     "dark:placeholder:text-text-secondary-dark dark:focus:border-primary",
            "placeholder": "Votre mot de passe"  # Placeholder text for the input
        }),
    )
    password2 = forms.CharField(
        label="Confirmez le mot de passe *",  # Label displayed to users
        strip=False,  # Don't strip whitespace from password
        widget=forms.PasswordInput(attrs={  # Password input widget with custom styling
            "class": "form-input h-14 w-full min-w-0 flex-1 resize-none overflow-hidden "
                     "rounded-lg border border-border-light bg-background-light p-3.5 pl-12 "
                     "text-base font-normal leading-normal text-text-light "
                     "placeholder:text-text-secondary-light focus:border-primary focus:outline-0 "
                     "focus:ring-2 focus:ring-primary/20 dark:border-border-dark "
                     "dark:bg-background-dark dark:text-text-dark "
                     "dark:placeholder:text-text-secondary-dark dark:focus:border-primary",
            "placeholder": "Confirmez votre mot de passe"  # Placeholder text for the input
        }),
    )

    class Meta:
        # Meta class to specify model and form fields
        model = User  # Use the custom User model
        # Fields to include in the form
        fields = ['email', 'username', 'role', 'deux_facteurs_active', 'password1', 'password2']
        # Custom labels for form fields
        labels = {
            'email': 'Email *',  # Label for email field
            'username': 'Nom d\'utilisateur *',  # Label for username field
        }
        # Custom widgets for form fields
        widgets = {
            'username': forms.TextInput(  # Text input widget with custom styling
                attrs={
                    "class": "form-input h-14 w-full min-w-0 flex-1 resize-none overflow-hidden "
                             "rounded-lg border border-border-light bg-background-light p-3.5 pl-12 "
                             "text-base font-normal leading-normal text-text-light "
                             "placeholder:text-text-secondary-light focus:border-primary focus:outline-0 "
                             "focus:ring-2 focus:ring-primary/20 dark:border-border-dark "
                             "dark:bg-background-dark dark:text-text-dark "
                             "dark:placeholder:text-text-secondary-dark dark:focus:border-primary",
                    'placeholder': 'nickosamba'  # Placeholder text for username field
                }),
            'email': forms.EmailInput(  # Email input widget with custom styling
                attrs={
                    "class": "form-input h-14 w-full min-w-0 flex-1 resize-none overflow-hidden "
                             "rounded-lg border border-border-light bg-background-light p-3.5 pl-12 "
                             "text-base font-normal leading-normal text-text-light "
                             "placeholder:text-text-secondary-light focus:border-primary focus:outline-0 "
                             "focus:ring-2 focus:ring-primary/20 dark:border-border-dark "
                             "dark:bg-background-dark dark:text-text-dark "
                             "dark:placeholder:text-text-secondary-dark dark:focus:border-primary",
                    'placeholder': 'example@gmail.com'  # Placeholder text for email field
                }),
            'deux_facteurs_active': forms.CheckboxInput(),  # Checkbox for 2FA
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def clean_role(self):
    #     role = self.cleaned_data.get("role")
    #     # Prevent registration with Administrator role
    #     if role == "Administrateur":
    #         raise forms.ValidationError("Vous ne pouvez pas choisir ce rôle.")
    #     return role

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Check if email already exists in the database
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé, veuillez en choisir un autre.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        # Check if both passwords are provided and match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2

    def save(self, commit=True):
        # Create the user instance without saving to database yet
        user = super().save(commit=False)
        # Set and hash the password using Django's built-in method
        user.set_password(self.cleaned_data["password1"])
        # Save the user to the database if commit is True
        if commit:
            user.save()
        return user


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize field labels to French
        self.fields['new_password1'].label = "Nouveau mot de passe *"
        self.fields['new_password2'].label = "Confirmer le nouveau mot de passe *"

        # Update widget attributes for consistent styling
        self.fields['new_password1'].widget.attrs.update({
            "class": "form-input h-14 w-full min-w-0 flex-1 resize-none overflow-hidden "
                     "rounded-lg border border-border-light bg-background-light p-3.5 pl-12 "
                     "text-base font-normal leading-normal text-text-light "
                     "placeholder:text-text-secondary-light focus:border-primary focus:outline-0 "
                     "focus:ring-2 focus:ring-primary/20 dark:border-border-dark "
                     "dark:bg-background-dark dark:text-text-dark "
                     "dark:placeholder:text-text-secondary-dark dark:focus:border-primary",
            'placeholder': 'Nouveau mot de passe'  # Placeholder for new password field
        })
        # Update widget attributes for confirm password field
        self.fields['new_password2'].widget.attrs.update({
            "class": "form-input h-14 w-full min-w-0 flex-1 resize-none overflow-hidden "
                     "rounded-lg border border-border-light bg-background-light p-3.5 pl-12 "
                     "text-base font-normal leading-normal text-text-light "
                     "placeholder:text-text-secondary-light focus:border-primary focus:outline-0 "
                     "focus:ring-2 focus:ring-primary/20 dark:border-border-dark "
                     "dark:bg-background-dark dark:text-text-dark "
                     "dark:placeholder:text-text-secondary-dark dark:focus:border-primary",
            'placeholder': 'Confirmez le mot de passe'  # Placeholder for confirm password field
        })
