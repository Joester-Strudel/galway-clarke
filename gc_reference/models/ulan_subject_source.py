# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanSubjectSource(SimpleBaseModel):
    subject = models.ForeignKey(
        "gc_reference.UlanSubject",
        on_delete=models.CASCADE,
        related_name="subject_sources",
    )
    source_id = models.CharField(
        max_length=255,
        help_text="Source_ID inside <Subject_Source>",
    )

    def __str__(self):
        return self.source_id

    class Meta:
        verbose_name = "ULAN Subject Source"
        verbose_name_plural = "ULAN Subject Sources"
