# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AatNote(SimpleBaseModel):
    subject = models.ForeignKey(
        "gc_definitions.AatSubject",
        on_delete=models.CASCADE,
        related_name="notes",
    )
    note_text = models.TextField()
    note_language = models.ForeignKey(
        "gc_definitions.IsoLanguage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Parsed from language field (e.g., '70051/English')",
    )


    # Model Methods
    def __str__(self):
        return f"{self.note_language}: {self.note_text[:50]}"

    # Model Metadata
    class Meta:
        verbose_name = "AAT Note"
        verbose_name_plural = "AAT Notes"
