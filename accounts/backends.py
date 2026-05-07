# accounts/backends.py

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailAuthBackend(ModelBackend):
    """
    Backend d'authentification personnalisé qui permet l'authentification par email.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Récupère l'utilisateur par email
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        
        # Vérifie le mot de passe
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        """
        Récupère un utilisateur par son ID.
        """
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None