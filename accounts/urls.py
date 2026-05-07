"""
Accounts App URL Configuration
This module defines all URL patterns for the accounts application.
It includes authentication URLs, dashboard, password reset functionality, and error handling.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as account_views
from .forms import CustomSetPasswordForm

# URL patterns for the accounts application
# Maps URL paths to their corresponding view functions
urlpatterns = [
    # path("dashboard/", account_views.dashboard_view, name="dashboard"),
    path("dashboard/", account_views.dashboard_router, name="dashboard"),
    path("register/", account_views.register_view, name="register"),   # User registration page
    path("", account_views.login_view, name="login"),            # User login page
    path("verify-otp/", account_views.verify_otp_view, name="verify_otp"),  # OTP verification for 2FA
    path("logout/", account_views.logout_view, name="logout"),         # User logout functionality

    path("password_reset/", account_views.CustomPasswordResetView.as_view(), name="password_reset"),

    # Step 2: Confirmation page after password reset email has been sent
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="registre/password_reset_done.html"
    ), name="password_reset_done"),

    # Step 3: Form to enter new password using token from email
    path("reset/<uidb64>/<token>/", account_views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    # Step 4: Final confirmation page after successful password reset
    path("reset/complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="registre/password_reset_complete.html"
    ), name="password_reset_complete"),

    # Error handling URLs
    # Custom error pages for specific HTTP errors
    path("403/", account_views.custom_permission_denied, name="custom_403"),  # Custom 403 error page
]