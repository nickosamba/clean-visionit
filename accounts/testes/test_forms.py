from django.test import TestCase
from accounts.forms import RegisterForm
from accounts.models import User

class RegisterFormTest(TestCase):
    def test_valid_form_creates_user(self):
        form_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "role": "Comptable",
            "deux_facteurs_active": False,
            "password1": "securepass123",
            "password2": "securepass123",
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        user = form.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, "newuser@example.com")
        self.assertTrue(user.check_password("securepass123"))

    def test_password_mismatch(self):
        form_data = {
            "email": "baduser@example.com",
            "username": "baduser",
            "role": "Comptable",
            "deux_facteurs_active": False,
            "password1": "securepass123",
            "password2": "wrongpass",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
        self.assertEqual(form.errors["password2"][0], "Les mots de passe ne correspondent pas.")

    def test_email_already_used(self):
        User.objects.create_user(
            email="dup@example.com",
            username="dupuser",
            password="securepass123",
            role="Comptable"
        )
        form_data = {
            "email": "dup@example.com",
            "username": "dupuser2",
            "role": "Comptable",
            "deux_facteurs_active": False,
            "password1": "securepass123",
            "password2": "securepass123",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(form.errors["email"][0], "Cet email est déjà utilisé, veuillez en choisir un autre.")

    # def test_role_administrateur_forbidden(self):
    #     form_data = {
    #         "email": "admin@example.com",
    #         "username": "adminuser",
    #         "role": "Administrateur",
    #         "deux_facteurs_active": False,
    #         "password1": "securepass123",
    #         "password2": "securepass123",
    #     }
    #     form = RegisterForm(data=form_data)
    #     self.assertFalse(form.is_valid())
    #     self.assertIn("role", form.errors)
    #     self.assertEqual(form.errors["role"][0], "Vous ne pouvez pas choisir ce rôle.")
    def test_role_administrateur_allowed(self):
        form_data = {
            "email": "admin@example.com",
            "username": "adminuser",
            "role": "Administrateur",
            "deux_facteurs_active": False,
            "password1": "securepass123",
            "password2": "securepass123",
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_missing_required_fields(self):
        form_data = {
            "email": "",
            "username": "",
            "role": "",
            "password1": "",
            "password2": "",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("username", form.errors)
        self.assertIn("role", form.errors)
