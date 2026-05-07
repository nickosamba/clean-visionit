from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import AuditLog, User

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user_with_email(self):
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="securepass123",
            role="Comptable"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.role, "Comptable")
        self.assertTrue(user.check_password("securepass123"))

    def test_str_method(self):
        user = User.objects.create_user(
            email="admin@example.com",
            username="admin",
            password="adminpass",
            role="Administrateur"
        )
        self.assertEqual(str(user), "admin@example.com (Administrateur)")

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="adminpass",
            role="Administrateur"
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
    
    def test_deux_facteurs_default(self):
        user = User.objects.create_user(
            email="gestion@example.com",
            username="gestion",
            password="gestionpass",
            role="Gestionnaire"
        )
        self.assertFalse(user.deux_facteurs_active)

    def test_deux_facteurs_enabled(self):
        user = User.objects.create_user(
            email="gestion2@example.com",
            username="gestion2",
            password="gestionpass",
            role="Gestionnaire",
            deux_facteurs_active=True
        )
        self.assertTrue(user.deux_facteurs_active)



class AuditLogModelTest(TestCase):
    def test_create_audit_log(self):
        user = User.objects.create_user(
            email="agent@example.com",
            username="agent",
            password="agentpass",
            role="Agent de terrain"
        )
        log = AuditLog.objects.create(
            utilisateur=user,
            action="Création",
            entite="Client",
            entite_id=1,
            details="Ajout d'un nouveau client",
            ip_address="127.0.0.1",
            device_info="Chrome"
        )
        self.assertEqual(log.utilisateur.email, "agent@example.com")
        self.assertEqual(log.action, "Création")
        self.assertEqual(log.entite, "Client")

    def test_audit_log_optional_fields(self):
        user = User.objects.create_user(
            email="opt@example.com",
            username="opt",
            password="optpass",
            role="Comptable"
        )
        log = AuditLog.objects.create(
            utilisateur=user,
            action="Suppression",
            entite="Facture"
        )
        self.assertIsNone(log.details)
        self.assertIsNone(log.ip_address)
        self.assertIsNone(log.device_info)
