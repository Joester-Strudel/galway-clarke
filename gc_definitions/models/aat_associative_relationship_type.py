# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AatAssociativeRelationshipType(SimpleBaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Relationship_Type value (e.g., 'distinguished from')",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "AAT Associative Relationship Type"
        verbose_name_plural = "AAT Associative Relationship Types"
