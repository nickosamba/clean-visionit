from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterViewTest(TestCase):
    def setUp(self):
        # Crée un admin pour accéder à la page
        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="adminpass",
            role="Administrateur"
        )
        self.client.login(email="admin@example.com", password="adminpass")

    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/create_user.html")

    def test_register_valid_user(self):
        response = self.client.post(reverse("register"), {
            "email": "newuser@example.com",
            "username": "newuser",
            "password1": "securepass123",
            "password2": "securepass123",
            "role": "Comptable"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("dashboard:users_list"))
        user = User.objects.filter(email="newuser@example.com").first()
        self.assertIsNotNone(user)

    def test_register_invalid_user(self):
        response = self.client.post(reverse("register"), {
            "email": "baduser@example.com",
            "username": "baduser",
            "password1": "securepass123",
            "password2": "wrongpass",
            "role": "Comptable"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Erreurs dans le formulaire, veuillez corriger.")
        user = User.objects.filter(email="baduser@example.com").first()
        self.assertIsNone(user)


class AccountsViewsTest(TestCase):
    def setUp(self):
        # Création d’un utilisateur de base
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="securepass123",
            role="Comptable",
            deux_facteurs_active=False
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_with_wrong_password(self):
        response = self.client.post(reverse("login"), {
            "email": "test@example.com",
            "password": "wrongpass"
        })
        # Vérifie que le message d’erreur attendu est bien présent
        self.assertContains(response, "Identifiants invalides ou compte inactif.")

    def test_login_with_correct_password_no_2fa(self):
        response = self.client.post(reverse("login"), {
            "email": "test@example.com",
            "password": "securepass123"
        })
        # Vérifie juste la redirection initiale
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("dashboard"))


    def test_login_with_correct_password_with_2fa(self):
        user2fa = User.objects.create_user(
            email="test2@example.com",
            username="testuser2",
            password="securepass123",
            role="Comptable",
            deux_facteurs_active=True
        )
        response = self.client.post(reverse("login"), {
            "email": "test2@example.com",
            "password": "securepass123"
        })
        # Redirection vers verify_otp
        self.assertRedirects(response, reverse("verify_otp"))

    def test_logout(self):
        self.client.login(email="test@example.com", password="securepass123")
        response = self.client.get(reverse("logout"))
        # Redirection vers login
        self.assertRedirects(response, reverse("login"))

    def test_password_reset_page_loads(self):
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registre/password_reset_form.html")

    def test_verify_otp_page_loads(self):
        response = self.client.get(reverse("verify_otp"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/verifie_otp.html")

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class DashboardPermissionsTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@example.com",
            username="admin",
            password="adminpass",
            role="Administrateur"
        )
        self.gestionnaire = User.objects.create_user(
            email="gestion@example.com",
            username="gestion",
            password="gestionpass",
            role="Gestionnaire"
        )
        self.agent = User.objects.create_user(
            email="agent@example.com",
            username="agent",
            password="agentpass",
            role="Agent de terrain"
        )
        self.comptable = User.objects.create_user(
            email="comptable@example.com",
            username="comptable",
            password="comptablepass",
            role="Comptable"
        )

    def test_admin_access(self):
        self.client.login(email="admin@example.com", password="adminpass")
        response = self.client.get(reverse("dashboard:admin"))
        self.assertEqual(response.status_code, 200)

    def test_gestionnaire_access(self):
        self.client.login(email="gestion@example.com", password="gestionpass")
        response = self.client.get(reverse("dashboard:gestionnaire"))
        self.assertEqual(response.status_code, 200)

    def test_agent_access(self):
        self.client.login(email="agent@example.com", password="agentpass")
        response = self.client.get(reverse("dashboard:agent"))
        self.assertEqual(response.status_code, 200)

    def test_comptable_access(self):
        self.client.login(email="comptable@example.com", password="comptablepass")
        response = self.client.get(reverse("dashboard:comptable"))
        self.assertEqual(response.status_code, 200)

    def test_restricted_access(self):
        # Un comptable ne doit pas accéder au dashboard admin
        self.client.login(email="comptable@example.com", password="comptablepass")
        response = self.client.get(reverse("dashboard:admin"))
        self.assertIn(response.status_code, [302, 403])
