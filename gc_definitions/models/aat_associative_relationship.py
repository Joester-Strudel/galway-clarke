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
    relationship_type = models.ForeignKey(
        "gc_definitions.AatAssociativeRelationshipType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="associative_relationships",
        help_text="Relationship_Type (e.g., 'distinguished from')",
    )
    related_subject = models.ForeignKey(
        "gc_definitions.AatSubject",
        on_delete=models.CASCADE,
        related_name="associative_relationships_to",
        help_text="VP_Subject_ID for the related concept",
    )
    historic_flag = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    # Model Methods
    def __str__(self):
        return f"{self.relationship_type} → {self.related_subject}"

    # Model Metadata
    class Meta:
        verbose_name = "AAT Associative Relationship"
        verbose_name_plural = "AAT Associative Relationships"
