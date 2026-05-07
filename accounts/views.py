from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (PasswordResetView,PasswordResetConfirmView)
from .forms import (LoginForm,RegisterForm,CustomSetPasswordForm)
from .models import User
from .utils import generate_otp  # Fonction utilitaire qui génère un code OTP
import time
from django.contrib.auth.decorators import login_required
from core.decorators import admin_required
from accounts.models import AuditLog    

@admin_required
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the new user to the database
            user = form.save()
            # 🔒 Créer un AuditLog pour l’inscription 
            AuditLog.objects.create(
                utilisateur=user, 
                action="Création", 
                entite="User", 
                entite_id=user.id )
            # Add success message to display to the user
            messages.success(request, "Compte créé avec succès, vous pouvez vous connecter.")
            # Redirect to login page after successful registration
            return redirect("dashboard:users_list")
        else:
            # Add error message if form validation fails
            messages.error(request, "Erreurs dans le formulaire, veuillez corriger.")
    else:
        # Create empty form for GET request
        form = RegisterForm()

    # Render registration template with form context
    #return render(request, "accounts/register.html", {"form": form})
    return render(request, "admin/create_user.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        # Process the login form data
        form = LoginForm(request.POST)
        if form.is_valid():
            # Extract email and password from cleaned form data
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            # Authenticate user with provided credentials
            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_active:
                # Check if user has two-factor authentication enabled
                if user.deux_facteurs_active:
                    # Generate OTP code for 2FA verification
                    otp = generate_otp()
                    # Store user ID, OTP code, and timestamp in session
                    request.session["otp_user_id"] = user.id
                    request.session["otp_code"] = otp
                    request.session["otp_timestamp"] = int(time.time())

                    # Send OTP code to user's email address
                    send_mail(
                        subject="🔐 Vérification de sécurité - Votre code OTP CLEAN",
                        message=(
                            f"Bonjour {user.username},\n\n"
                            f"Voici votre code OTP : {otp}\n\n"
                            "⚠️ Ce code est valable uniquement pendant 5 minutes.\n"
                            "Ne le partagez jamais.\n\n"
                            "Merci d'utiliser CLEAN.\n"
                            "L'équipe Sécurité"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                    )
                    # Inform user that OTP has been sent
                    messages.info(request, "Un code OTP vous a été envoyé par email.")
                    # Redirect to OTP verification page
                    return redirect("verify_otp")
                else:
                    # Perform direct login since 2FA is not enabled
                    login(request, user)
                    # Add success message for successful login
                    messages.success(request, "Connecté.")
                    # 🔒 Créer un AuditLog pour la connexion 
                    AuditLog.objects.create(
                        utilisateur=user, 
                        action="Connexion", 
                        entite="User", 
                        entite_id=user.id 
                    )
                    # Redirect to dashboard after successful login
                    return redirect("dashboard")
            else:
                # Add error to form if authentication fails
                form.add_error(None, "Identifiants invalides ou compte inactif.")
    else:
        # Create empty form for GET request
        form = LoginForm()

    # Render login template with form context
    return render(request, "accounts/login.html", {"form": form})


def verify_otp_view(request):
    if request.method == "POST":
        # Get OTP code from POST data and clean whitespace
        code = request.POST.get("otp", "").strip()
        # Retrieve stored OTP data from session
        user_id = request.session.get("otp_user_id")
        otp_code = request.session.get("otp_code")
        otp_timestamp = request.session.get("otp_timestamp")

        # Validate that all required session data exists
        if not user_id or not otp_code or not otp_timestamp:
            messages.error(request, "Session OTP invalide ou expirée. Veuillez vous reconnecter.")
            return redirect("login")

        # Check if OTP code has expired (5 minutes = 300 seconds)
        if int(time.time()) - int(otp_timestamp) > 300:
            messages.error(request, "⏳ Code OTP expiré. Veuillez vous reconnecter.")
            # Clean up expired session data
            request.session.pop("otp_user_id", None)
            request.session.pop("otp_code", None)
            request.session.pop("otp_timestamp", None)
            return redirect("login")

        # Verify that the entered code matches the stored OTP code
        if code == str(otp_code):
            try:
                # Retrieve user from database using stored user ID
                user = User.objects.get(id=user_id)
                # Perform login with verified user
                login(request, user)
                # Clean up session data after successful verification
                request.session.pop("otp_user_id", None)
                request.session.pop("otp_code", None)
                request.session.pop("otp_timestamp", None)
                # Add success message for successful authentication
                messages.success(request, "Authentification réussie ! Bienvenue.")
                # Redirect to dashboard after successful 2FA verification
                return redirect("dashboard")
            except User.DoesNotExist:
                # Handle case where user was deleted after OTP generation
                messages.error(request, "Utilisateur introuvable. Veuillez vous reconnecter.")
                return redirect("login")
        else:
            # Add error message if OTP code is invalid
            messages.error(request, "Code OTP invalide")
            # Re-render verification page with error message
            return render(request, "accounts/verifie_otp.html")

    # Render OTP verification template for GET request
    return render(request, "accounts/verifie_otp.html")


def logout_view(request):
    # Perform logout operation, clearing user session
    logout(request)
    # Add informational message about successful logout
    messages.info(request, "Déconnecté.")
    # Redirect user to login page after logout
    return redirect("login")


@login_required
def dashboard_router(request):
    role = request.user.role

    if role == "Administrateur":
        return redirect("dashboard:admin")

    if role == "Gestionnaire":
        return redirect("dashboard:gestionnaire")

    if role == "Agent de terrain":
        return redirect("dashboard:agent")

    if role == "Comptable":
        return redirect("dashboard:comptable")

    # fallback
    return redirect("dashboard:gestionnaire")


def custom_permission_denied(request, exception=None):
    # Render custom 403 error page with appropriate HTTP status code
    return render(request, "errors/403.html", status=403)


class CustomPasswordResetView(PasswordResetView):
    # Template for the password reset form
    template_name = "registre/password_reset_form.html"
    # Template for the password reset email (plain text)
    email_template_name = "registre/password_reset_email.txt"
    # Template for the password reset email (HTML version)
    html_email_template_name = "registre/password_reset_email.html"
    # Template for the email subject line
    subject_template_name = "registre/password_reset_subject.txt"

# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     # Template for the password reset confirmation form
#     template_name = "registre/password_reset_confirm.html"
#     # Custom form class to apply consistent styling
#     form_class = CustomSetPasswordForm
#     # URL to redirect to after successful password reset
#     success_url = reverse_lazy("password_reset_complete")
from accounts.models import AuditLog
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registre/password_reset_confirm.html"
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("password_reset_complete")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = getattr(form, "user", None) or self.get_user()
        if user:
            AuditLog.objects.create(
                utilisateur=user,
                action="Réinitialisation mot de passe",
                entite="User",
                entite_id=user.id
            )
        return response
