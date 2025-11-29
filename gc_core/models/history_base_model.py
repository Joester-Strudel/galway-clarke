# Python Imports
import uuid

# Django Imports
from django.db import models
from django.conf import settings

# Third-Party Imports
from simple_history.models import HistoricalRecords


class HistoryBaseModel(models.Model):
    """
    Base model providing:
    - UUID primary key
    - created_at timestamp
    - last_updated_at timestamp
    - created_by user tracking
    - simple_history tracking
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        null=False,
        blank=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name="Created At",
    )

    last_updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name="Last Updated",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        verbose_name="Created By",
        help_text="User who created this record.",
    )

    # inherit=True propagates history to concrete subclasses without warning
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
