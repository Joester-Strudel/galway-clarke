# Python Imports
import uuid
import secrets

# Django Imports
from django.db import models

# Third-Party Imports
from simple_history.models import HistoricalRecords


class ApiKey(models.Model):
    # Fields
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        null=False,
        blank=False,
        editable=False,
    )
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
    tenants = models.ManyToManyField(
        "ri_tenants.Tenant",
        blank=True,
        verbose_name="Tenants",
        help_text="The tenants associated with this API key.",
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
        "ri_users.ApiRoute",
        blank=True,
        verbose_name="Allowed Routes",
    )

    # Metadata
    history = HistoricalRecords()
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name="Created",
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name="Last Updated",
    )

    # Model Methods
    def __str__(self):
        return self.name

    def regenerate_keys(self):
        """
        Regenerate both the API key and secret key.
        """
        self.key = secrets.token_urlsafe(48)
        self.save()

    def save(self, *args, **kwargs):
        """
        Ensure key and secret are generated on creation.
        """
        if not self.key:
            self.key = secrets.token_urlsafe(48)  # Generates a secure 64-character API key
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"
        ordering = ("end_date",)