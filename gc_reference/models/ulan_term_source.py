# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanTermSource(SimpleBaseModel):
    term = models.ForeignKey(
        "gc_reference.UlanTerm",
        on_delete=models.CASCADE,
        related_name="sources",
    )
    source_id = models.CharField(
        max_length=255,
    )
    page = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    preferred_flag = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.source_id

    class Meta:
        verbose_name = "ULAN Term Source"
        verbose_name_plural = "ULAN Term Sources"
