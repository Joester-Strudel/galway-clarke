# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AATTermContributor(SimpleBaseModel):
    term = models.ForeignKey(
        "gc_collections.AATTerm",
        on_delete=models.CASCADE,
        related_name="contributors",
    )
    contributor_id = models.CharField(
        max_length=100,
        help_text="Contributor_id for a term",
    )
    preferred_flag = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Preferred, Non Preferred, etc.",
    )

    # Model Methods
    def __str__(self):
        return self.contributor_id
