# Python Imports
import secrets

# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import HistoryBaseModel


class Organization(HistoryBaseModel):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Name",
        help_text="The name of this organization.",
    )

    # Model Methods
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ("name",)
