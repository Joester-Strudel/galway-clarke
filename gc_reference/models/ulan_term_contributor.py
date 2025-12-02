# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanTermContributor(SimpleBaseModel):
    term = models.ForeignKey(
        "gc_reference.UlanTerm",
        on_delete=models.CASCADE,
        related_name="contributors",
    )
    contributor_id = models.CharField(
        max_length=100,
    )
    preferred_flag = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.contributor_id

    class Meta:
        verbose_name = "ULAN Term Contributor"
        verbose_name_plural = "ULAN Term Contributors"
