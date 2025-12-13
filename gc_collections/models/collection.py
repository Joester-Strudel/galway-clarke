# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import HistoryBaseModel


class Collection(HistoryBaseModel):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Name",
        help_text="The name of this collection.",
    )
    organization = models.ForeignKey(
        "gc_users.Team",
        on_delete=models.CASCADE,
        related_name="collections",
        verbose_name="Team",
        help_text="The team this collection belongs to.",
    )

    # Model Methods
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
        ordering = ("name",)
