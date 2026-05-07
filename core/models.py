from django.db import models

# Create your models here.
class Setting(models.Model):
    """
    Model representing user-specific application settings.
    Stores preferences like theme selection for individual users.
    """
    # One-to-one relationship with the User model
    user = models.OneToOneField(
        'accounts.User',  # Reference to the custom User model
        on_delete=models.CASCADE,  # Delete settings if user is deleted
        related_name='setting',  # Reverse relationship name
        verbose_name="Utilisateur"  # Field label for admin interface
    )
    # Theme preference for the application interface
    theme = models.CharField(
        max_length=20,  # Maximum length of 20 characters
        choices=[  # Available theme options
            ('light', 'light'),   # Light theme
            ('dark', 'dark'),     # Dark theme
            ('default', 'default')  # Default theme
        ],
        default='default'  # Default to default theme
    )

    def __str__(self):
        """
        String representation of the Setting model.

        Returns:
            str: Description of the settings object
        """
        return f"Paramètres de l'application"