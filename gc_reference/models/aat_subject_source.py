# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AatSubjectSource(SimpleBaseModel):
    subject = models.ForeignKey(
        "gc_reference.AatSubject",
        on_delete=models.CASCADE,
        related_name="subject_sources",
    )
    source_id = models.CharField(
        max_length=255,
        help_text="Source_ID inside <Subject_Source>",
    )

    # Model Methods
    def __str__(self):
        return self.source_id

    # Model Metadata
    class Meta:
        verbose_name = "AAT Subject Source"
        verbose_name_plural = "AAT Subject Sources"
