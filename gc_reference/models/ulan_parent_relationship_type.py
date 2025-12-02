# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanParentRelationshipType(SimpleBaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Hier_Rel_Type (e.g. Instance-BTI)",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ULAN Parent Relationship Type"
        verbose_name_plural = "ULAN Parent Relationship Types"
