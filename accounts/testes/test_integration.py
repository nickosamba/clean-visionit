import re
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import AuditLog
from django.core import mail
from accounts.forms import RegisterForm


User = get_user_model()

class AccountsIntegrationTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="adminpass123",
            role="Administrateur"
        )

    def test_register_user(self):
        self.client.login(email="admin@example.com", password="adminpass123")
        response = self.client.post(reverse("register"), {
            "email": "newuser@example.com",
            "username": "newuser",
            "role": "Comptable",
            "password1": "securepass123",
            "password2": "securepass123",
        }, follow=True)

        user = User.objects.filter(email="newuser@example.com").first()
        self.assertIsNotNone(user)

    def test_audit_log_on_register(self):
        self.client.login(email="admin@example.com", password="adminpass123")
        response = self.client.post(reverse("register"), {
            "email": "auditregister@example.com",
            "username": "auditregister",
            "role": "Comptable",
            "password1": "securepass123",
            "password2": "securepass123",
        }, follow=True)

        user = User.objects.filter(email="auditregister@example.com").first()
        self.assertIsNotNone(user, "Utilisateur non créé")

        log = AuditLog.objects.filter(utilisateur=user, action="Création").first()
        self.assertIsNotNone(log, "AuditLog non créé pour l’inscription")
        self.assertEqual(log.entite, "User")
        self.assertEqual(log.entite_id, user.id)

    def test_login_with_2fa(self):
        # Créer un utilisateur avec 2FA activé
        user = User.objects.create_user(
            email="twofa@example.com",
            username="twofa",
            password="securepass123",
            role="Comptable",
            deux_facteurs_active=True
        )

        # Étape 1 : login avec email + mot de passe
        response = self.client.post(reverse("login"), {
            "email": "twofa@example.com",
            "password": "securepass123",
        })

        # Vérifier qu’un OTP est envoyé par email
        self.assertEqual(len(mail.outbox), 1, "OTP non envoyé par email")
        otp_email = mail.outbox[0]
        self.assertIn("Votre code OTP", otp_email.subject, f"Sujet inattendu: {otp_email.subject}")

        # Simuler validation OTP (exemple : code '123456')
        response = self.client.post(reverse("verify_otp"), {
            "email": "twofa@example.com",
            "otp_code": "123456",
        }, follow=True)


        # Vérifier que l’utilisateur accède au dashboard
        self.assertContains(response, "Vérification OTP")


    import re

def test_password_reset_creates_audit_log(self):
    user = User.objects.create_user(
        email="resetuser@example.com",
        username="resetuser",
        password="oldpass123",
        role="Comptable"
    )

    # Étape 1 : demander un reset
    self.client.post(reverse("password_reset"), {"email": "resetuser@example.com"})
    self.assertEqual(len(mail.outbox), 1)

    # Étape 2 : extraire l’URL de reset depuis l’email
    reset_email = mail.outbox[0]
    url_match = re.search(r"http://testserver(/[\w/-]+)", reset_email.body)
    self.assertIsNotNone(url_match, "Lien de reset non trouvé dans l’email")
    reset_url = url_match.group(1)

    # Étape 3 : GET sur l’URL pour charger le formulaire
    response = self.client.get(reset_url)
    self.assertEqual(response.status_code, 200)

    # Étape 4 : POST avec un nouveau mot de passe
    response = self.client.post(reset_url, {
        "new_password1": "newpass123",
        "new_password2": "newpass123",
    }, follow=True)
    self.assertEqual(response.status_code, 200)

    # Étape 5 : vérifier l’AuditLog
    log = AuditLog.objects.filter(utilisateur=user, action="Réinitialisation mot de passe").first()
    self.assertIsNotNone(log, "AuditLog non créé pour le reset password")


def test_login_with_invalid_otp(self):
    user = User.objects.create_user(
        email="otpuser@example.com",
        username="otpuser",
        password="securepass123",
        role="Comptable",
        deux_facteurs_active=True
    )

    # Login → envoi OTP
    self.client.post(reverse("login"), {"email": "otpuser@example.com", "password": "securepass123"})
    self.assertEqual(len(mail.outbox), 1)

    # Vérification avec mauvais code
    response = self.client.post(reverse("verify_otp"), {
        "email": "otpuser@example.com",
        "otp_code": "000000",  # faux code
    }, follow=True)

    self.assertContains(response, "Code OTP invalide")
    log = AuditLog.objects.filter(utilisateur=user, action="Connexion").first()
    self.assertIsNone(log, "AuditLog ne doit pas être créé avec un OTP invalide")

def test_admin_can_access_register(self):
    admin = User.objects.create_superuser(
        email="admin@example.com",
        username="admin",
        password="adminpass123",
        role="Administrateur"
    )
    self.client.login(email="admin@example.com", password="adminpass123")
    response = self.client.get(reverse("register"))
    self.assertEqual(response.status_code, 200)

def test_comptable_cannot_access_register(self):
    comptable = User.objects.create_user(
        email="comp@example.com",
        username="comp",
        password="comp123",
        role="Comptable"
    )
    self.client.login(email="comp@example.com", password="comp123")
    response = self.client.get(reverse("register"))
    self.assertNotEqual(response.status_code, 200)  # doit être 403 ou redirection

def test_unauthenticated_redirects_to_login(self):
    response = self.client.get(reverse("register"))
    self.assertEqual(response.status_code, 302)
    self.assertIn(reverse("login"), response.url)




def test_admin_creates_user_generates_audit_log(self):
    admin = User.objects.create_superuser(
        email="admin@example.com",
        username="admin",
        password="adminpass123",
        role="Administrateur"
    )
    self.client.login(email="admin@example.com", password="adminpass123")

    response = self.client.post(reverse("register"), {
        "email": "newuser@example.com",
        "username": "newuser",
        "role": "Comptable",
        "password1": "securepass123",
        "password2": "securepass123",
    }, follow=True)

    user = User.objects.filter(email="newuser@example.com").first()
    self.assertIsNotNone(user, "Utilisateur non créé par admin")

    log = AuditLog.objects.filter(utilisateur=user, action="Création").first()
    self.assertIsNotNone(log, "AuditLog non créé par admin lors de l’inscription")


def test_comptable_cannot_create_user_and_no_audit_log(self):
    comptable = User.objects.create_user(
        email="comp@example.com",
        username="comp",
        password="comp123",
        role="Comptable"
    )
    self.client.login(email="comp@example.com", password="comp123")

    response = self.client.post(reverse("register"), {
        "email": "blockeduser@example.com",
        "username": "blockeduser",
        "role": "Comptable",
        "password1": "securepass123",
        "password2": "securepass123",
    }, follow=True)

    # Vérifier que l’utilisateur n’est pas créé
    user = User.objects.filter(email="blockeduser@example.com").first()
    self.assertIsNone(user, "Utilisateur créé par comptable alors que ce n’est pas autorisé")

    # Vérifier qu’aucun AuditLog n’est généré
    log = AuditLog.objects.filter(action="Création", entite="User").first()
    self.assertIsNone(log, "AuditLog ne doit pas être créé par comptable")

def test_admin_login_creates_audit_log(self):
    admin = User.objects.create_superuser(
        email="adminlogin@example.com",
        username="adminlogin",
        password="adminpass123",
        role="Administrateur"
    )
    self.client.post(reverse("login"), {
        "email": "adminlogin@example.com",
        "password": "adminpass123",
    }, follow=True)

    log = AuditLog.objects.filter(utilisateur=admin, action="Connexion").first()
    self.assertIsNotNone(log, "AuditLog non créé pour login admin")


def test_admin_logout_creates_audit_log(self):
    admin = User.objects.create_superuser(
        email="adminlogout@example.com",
        username="adminlogout",
        password="adminpass123",
        role="Administrateur"
    )
    self.client.login(email="adminlogout@example.com", password="adminpass123")
    self.client.get(reverse("logout"), follow=True)

    log = AuditLog.objects.filter(utilisateur=admin, action="Déconnexion").first()
    self.assertIsNotNone(log, "AuditLog non créé pour logout admin")


def test_comptable_login_logout_creates_audit_log(self):
    comptable = User.objects.create_user(
        email="complog@example.com",
        username="complog",
        password="comp123",
        role="Comptable"
    )
    self.client.post(reverse("login"), {
        "email": "complog@example.com",
        "password": "comp123",
    }, follow=True)

    login_log = AuditLog.objects.filter(utilisateur=comptable, action="Connexion").first()
    self.assertIsNotNone(login_log, "AuditLog non créé pour login comptable")

    self.client.get(reverse("logout"), follow=True)
    logout_log = AuditLog.objects.filter(utilisateur=comptable, action="Déconnexion").first()
    self.assertIsNotNone(logout_log, "AuditLog non créé pour logout comptable")
def test_enable_2fa_creates_audit_log(self):
    user = User.objects.create_user(
        email="twofauser@example.com",
        username="twofauser",
        password="securepass123",
        role="Comptable"
    )
    self.client.login(email="twofauser@example.com", password="securepass123")

    # Activer le 2FA
    response = self.client.post(reverse("enable_2fa"), {}, follow=True)
    self.assertEqual(response.status_code, 200)

    # Vérifier que l’AuditLog est créé
    log = AuditLog.objects.filter(utilisateur=user, action="Activation 2FA").first()
    self.assertIsNotNone(log, "AuditLog non créé lors de l’activation du 2FA")


def test_disable_2fa_creates_audit_log(self):
    user = User.objects.create_user(
        email="twofauser2@example.com",
        username="twofauser2",
        password="securepass123",
        role="Comptable",
        deux_facteurs_active=True
    )
    self.client.login(email="twofauser2@example.com", password="securepass123")

    # Désactiver le 2FA
    response = self.client.post(reverse("disable_2fa"), {}, follow=True)
    self.assertEqual(response.status_code, 200)

    # Vérifier que l’AuditLog est créé
    log = AuditLog.objects.filter(utilisateur=user, action="Désactivation 2FA").first()
    self.assertIsNotNone(log, "AuditLog non créé lors de la désactivation du 2FA")
