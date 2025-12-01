# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanSubjectContributor(SimpleBaseModel):
    subject = models.ForeignKey(
        "gc_definitions.UlanSubject",
        on_delete=models.CASCADE,
        related_name="subject_contributors",
    )
    contributor_id = models.CharField(
        max_length=100,
        help_text="Contributor_id within <Subject_Contributor>",
    )

    def __str__(self):
        return self.contributor_id

    class Meta:
        verbose_name = "ULAN Subject Contributor"
        verbose_name_plural = "ULAN Subject Contributors"