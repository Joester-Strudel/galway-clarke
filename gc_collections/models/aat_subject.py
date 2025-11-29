# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AATSubject(SimpleBaseModel):
    aat_id = models.CharField(
        max_length=32,
        unique=True,
        help_text="Getty AAT Subject_ID",
    )
    record_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Record_Type field (e.g., 'Concept')",
    )
    merged_status = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Merged_Status field",
    )
    sort_order = models.IntegerField(
        null=True,
        blank=True,
        help_text="Sort_Order",
    )
    parent_aat_id = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        help_text="Preferred Parent_Subject_ID",
    )
    parent_string = models.TextField(
        null=True,
        blank=True,
        help_text="Parent_String listing hierarchy ancestors",
    )
    parent_relationship_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Hier_Rel_Type (e.g., 'Genus/Species-BTG')",
    )

    # Model Methods
    def __str__(self):
        return self.aat_id
