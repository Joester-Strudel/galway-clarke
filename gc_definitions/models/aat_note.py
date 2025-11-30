# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AATNote(SimpleBaseModel):
    subject = models.ForeignKey(
        "gc_definitions.AATSubject",
        on_delete=models.CASCADE,
        related_name="notes",
    )
    note_text = models.TextField()
    note_language = models.CharField(
        max_length=100,
        help_text="Language of note text (e.g., English, Spanish, Dutch)",
    )

    # Model Methods
    def __str__(self):
        return f"{self.note_language}: {self.note_text[:50]}"

    # Model Metadata
    class Meta:
        verbose_name = "AAT Note"
        verbose_name_plural = "AAT Notes"
