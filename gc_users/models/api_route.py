# Python Imports
import uuid

# Django Imports
from django.db import models

# Third-Party Imports
from simple_history.models import HistoricalRecords


class ApiRoute(models.Model):
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
        unique=True,
        blank=False,
        null=False,
        verbose_name="Name",
        help_text="A human-readable name for this API key.",
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

    class Meta:
        ordering = ("name",)
        verbose_name = "API Route"
        verbose_name_plural = "API Routes"