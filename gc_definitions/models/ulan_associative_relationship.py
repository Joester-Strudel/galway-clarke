# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanAssociativeRelationship(SimpleBaseModel):
    subject = models.ForeignKey(
        "gc_definitions.UlanSubject",
        on_delete=models.CASCADE,
        related_name="associative_relationships",
    )
    relationship_type = models.ForeignKey(
        "gc_definitions.UlanAssociativeRelationshipType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="associative_relationships",
    )
    related_subject = models.ForeignKey(
        "gc_definitions.UlanSubject",
        on_delete=models.CASCADE,
        related_name="associative_relationships_to",
        help_text="Related ULAN subject",
    )
    historic_flag = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    display_date = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Display_Date inside <AR_Date>",
    )
    start_date = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    end_date = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.relationship_type} → {self.related_subject}"

    class Meta:
        verbose_name = "ULAN Associative Relationship"
        verbose_name_plural = "ULAN Associative Relationships"
