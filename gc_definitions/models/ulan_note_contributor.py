# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanNoteContributor(SimpleBaseModel):
    note = models.ForeignKey(
        "gc_definitions.UlanNote",
        on_delete=models.CASCADE,
        related_name="contributors",
    )
    contributor_id = models.CharField(
        max_length=100,
        help_text="Contributor_id inside <Note_Contributor>",
    )

    def __str__(self):
        return self.contributor_id

    class Meta:
        verbose_name = "ULAN Note Contributor"
        verbose_name_plural = "ULAN Note Contributors"