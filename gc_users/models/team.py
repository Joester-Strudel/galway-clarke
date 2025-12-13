# Django Imports
from django.conf import settings
from django.db import models

# First-Party Imports
from gc_core.models import HistoryBaseModel


class Team(HistoryBaseModel):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
        verbose_name="Name",
        help_text="The name of this organization.",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="owned_organizations",
        null=True,
        blank=True,
        help_text="User who owns this organization.",
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="organizations",
        blank=True,
        help_text="Users who belong to this organization.",
    )

    # Model Methods
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        ordering = ("name",)
