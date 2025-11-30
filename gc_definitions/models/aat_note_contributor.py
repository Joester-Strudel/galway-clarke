# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AATNoteContributor(SimpleBaseModel):
    note = models.ForeignKey(
        "gc_collections.AATNote",
        on_delete=models.CASCADE,
        related_name="contributors",
    )
    contributor_id = models.CharField(
        max_length=100,
        help_text="Contributor ID for descriptive note",
    )

    # Model Methods
    def __str__(self):
        return self.contributor_id

    # Model Metadata
    class Meta:
        verbose_name = "AAT Note Contributor"
        verbose_name_plural = "AAT Note Contributors"
