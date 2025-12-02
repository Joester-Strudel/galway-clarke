# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AatParentRelationshipType(SimpleBaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Parent relationship type (e.g., 'Genus/Species-BTG')",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "AAT Parent Relationship Type"
        verbose_name_plural = "AAT Parent Relationship Types"
