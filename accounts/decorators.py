# accounts/decorators.py

from django.core.exceptions import PermissionDenied

def role_required(roles):
    """
    🎯 Décorateur pour restreindre l'accès à une vue selon le rôle utilisateur.

    - Vérifie que l'utilisateur est authentifié.
    - Vérifie que son rôle figure dans la liste des rôles autorisés.
    - Si ce n'est pas le cas → lève une exception PermissionDenied (erreur 403).

    Args:
        roles (list[str]): Liste des rôles autorisés (ex: ["Administrateur", "Gestionnaire"]).

    Returns:
        function: La vue décorée, protégée par la vérification des rôles.
    """
    def decorator(view_func):
        def _wrapped(request, *args, **kwargs):
            # Vérifie authentification et rôle
            if not request.user.is_authenticated or request.user.role not in roles:
                raise PermissionDenied
            # Si OK → exécute la vue
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


# ============================================================
# 📌 Exemple d'utilisation
# ============================================================
# from .decorators import role_required
#
# @role_required(["Administrateur", "Gestionnaire"])
# def my_view(request):
#     # Cette vue est accessible uniquement aux admins et gestionnaires
#     ...
