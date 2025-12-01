# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanNote(SimpleBaseModel):
    subject = models.ForeignKey(
        "gc_definitions.UlanSubject",
        on_delete=models.CASCADE,
        related_name="notes",
    )
    note_text = models.TextField()
    note_language = models.ForeignKey(
        "gc_definitions.IsoLanguage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Parsed from <Note_Language>",
    )

    def __str__(self):
        return self.note_text[:50]

    class Meta:
        verbose_name = "ULAN Note"
        verbose_name_plural = "ULAN Notes"