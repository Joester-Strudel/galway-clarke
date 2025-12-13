# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class State(SimpleBaseModel):
    """State/region record."""

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="State",
    )
    abbreviation = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        verbose_name="Abbreviation",
        help_text="Two-letter state abbreviation.",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ("name",)
