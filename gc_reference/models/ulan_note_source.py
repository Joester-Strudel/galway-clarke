# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanNoteSource(SimpleBaseModel):
    note = models.ForeignKey(
        "gc_reference.UlanNote",
        on_delete=models.CASCADE,
        related_name="sources",
    )
    source_id = models.CharField(
        max_length=255,
        help_text="Source_ID inside <Note_Source>",
    )

    def __str__(self):
        return self.source_id

    class Meta:
        verbose_name = "ULAN Note Source"
        verbose_name_plural = "ULAN Note Sources"
