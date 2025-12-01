# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AatAssociativeRelationship(SimpleBaseModel):
    subject = models.ForeignKey(
        "gc_definitions.AatSubject",
        on_delete=models.CASCADE,
        related_name="associative_relationships",
    )
    relationship_type = models.CharField(
        max_length=100,
        help_text="Relationship_Type (e.g., 'distinguished from')",
    )
    related_aat_id = models.CharField(
        max_length=32,
        help_text="VP_Subject_ID for the related concept",
    )
    historic_flag = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    # Model Methods
    def __str__(self):
        return f"{self.relationship_type} → {self.related_aat_id}"

    # Model Metadata
    class Meta:
        verbose_name = "AAT Associative Relationship"
        verbose_name_plural = "AAT Associative Relationships"
