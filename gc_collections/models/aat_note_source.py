# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AATNoteSource(SimpleBaseModel):
    note = models.ForeignKey(
        "gc_collections.AATNote",
        on_delete=models.CASCADE,
        related_name="sources",
    )
    source_id = models.CharField(
        max_length=255,
        help_text="Source reference for note text",
    )

    # Model Methods
    def __str__(self):
        return self.source_id

    # Model Metadata
    class Meta:
        verbose_name = "AAT Note Source"
        verbose_name_plural = "AAT Note Sources"
