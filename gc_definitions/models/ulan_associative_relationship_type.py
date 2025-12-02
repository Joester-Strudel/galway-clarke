# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanAssociativeRelationshipType(SimpleBaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Relationship type label for ULAN associative relationships",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ULAN Associative Relationship Type"
        verbose_name_plural = "ULAN Associative Relationship Types"
