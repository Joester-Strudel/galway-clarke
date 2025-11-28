from django.apps import AppConfig


class GcUsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gc_users"

    def ready(self):
        # Ensure admin classes are registered when the app is ready.
        from . import admin  # noqa: F401

    verbose_name = "User Management"
