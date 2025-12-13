# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel
from gc_core.constants.colors import TAILWIND_COLOR_CHOICES


class Status(SimpleBaseModel):
    # Fields
    team = models.ForeignKey(
        "gc_users.Team",
        on_delete=models.CASCADE,
        related_name="crm_statuses",
        verbose_name="Team",
        help_text="Team that owns this status definition.",
    )
    name = models.CharField(
        max_length=80,
        blank=False,
        null=False,
        verbose_name="Name",
        help_text="Lifecycle status (active, pending, churn risk, etc.).",
    )
    color = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        verbose_name="Color",
        help_text="Optional hex or token to style this status.",
        choices=TAILWIND_COLOR_CHOICES,
        default="gray",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
    )

    # Model Methods
    def __str__(self):
        return self.name

    # Model Metadata
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
        ordering = ("name",)
