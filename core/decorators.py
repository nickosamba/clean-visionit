from functools import wraps
from django.core.exceptions import PermissionDenied

def role_required(required_role):
    """Décorateur générique basé sur le champ role"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role == required_role:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator

# Décorateurs spécifiques
def agent_required(view_func):
    return role_required("Agent de terrain")(view_func)

def comptable_required(view_func):
    return role_required("Comptable")(view_func)

def gestionnaire_required(view_func):
    return role_required("Gestionnaire")(view_func)

def admin_required(view_func):
    return role_required("Administrateur")(view_func)
