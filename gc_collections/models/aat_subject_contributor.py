# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AATSubjectContributor(SimpleBaseModel):
    subject = models.ForeignKey(
        "gc_collections.AATSubject",
        on_delete=models.CASCADE,
        related_name="subject_contributors",
    )
    contributor_id = models.CharField(
        max_length=100,
        help_text="Contributor_id inside <Subject_Contributor>",
    )

    # Model Methods
    def __str__(self):
        return self.contributor_id

    # Model Metadata
    class Meta:
        verbose_name = "AAT Subject Contributor"
        verbose_name_plural = "AAT Subject Contributors"
