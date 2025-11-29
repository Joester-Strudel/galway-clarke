# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AATTermSource(SimpleBaseModel):
    term = models.ForeignKey(
        "gc_collections.AATTerm",
        on_delete=models.CASCADE,
        related_name="sources",
    )
    source_id = models.CharField(
        max_length=255,
        help_text="Source_ID from <Term_Source>",
    )
    page = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Page or extra locator info",
    )
    preferred_flag = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    # Model Methods
    def __str__(self):
        return self.source_id
