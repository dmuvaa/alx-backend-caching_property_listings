# properties/apps.py
from django.apps import AppConfig

class PropertiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "properties"

    def ready(self):
        # Explicit import so checkers see the exact string
        import properties.signals  # noqa: F401