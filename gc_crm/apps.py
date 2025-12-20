# Django Imports
from django.apps import AppConfig


class GcCrmConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gc_crm"

    def ready(self):
        # Import signal handlers
        from . import signals  # noqa: F401
