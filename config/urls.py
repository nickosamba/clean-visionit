# clean_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),
    path("clients/", include("clients.urls")),
    path("dashboard/", include("core.urls")),
    # path("incidents/", include("incidents.urls")),
    path("paiements/", include("paiements.urls")),
    path("tournees/", include("tournees.urls")),
    path("abonnements/", include("abonnements.urls")),
    path("secteurs/", include("secteurs.urls")),
    path("agents/", include("agents.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)