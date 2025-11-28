# Python Imports
import secrets

# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import HistoryBaseModel


class ApiKey(HistoryBaseModel):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Name",
        help_text="A human-readable name for this API key.",
    )
    key = models.CharField(
        max_length=64,
        unique=True,
        blank=False,
        null=False,
        verbose_name="API Key",
        help_text="The unique API key used for authentication.",
    )
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name="IP Address",
        help_text="Optional static IP address. If set, requests must come from this IP.",
    )
    start_date = models.DateTimeField(
        blank=False,
        null=False,
        verbose_name="Start Date",
        help_text="The date and time when this API key becomes valid.",
    )
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="End Date",
        help_text="The date and time when this API key expires.",
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Indicates whether this API key is currently active.",
    )
    routes = models.ManyToManyField(
        "gc_users.ApiRoute",
        blank=True,
        verbose_name="Allowed Routes",
    )

    # Model Methods
    def __str__(self):
        return self.name

    def regenerate_keys(self):
        """Regenerate the API key."""
        self.key = secrets.token_urlsafe(48)
        self.save()

    def save(self, *args, **kwargs):
        """Generate API key on creation."""
        if not self.key:
            self.key = secrets.token_urlsafe(48)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"
        ordering = ("end_date",)
