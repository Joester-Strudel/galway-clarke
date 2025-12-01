# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanSubject(SimpleBaseModel):
    ulan_id = models.CharField(
        max_length=32,
        unique=True,
        help_text="Getty ULAN Subject_ID",
    )
    record_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Record_Type (e.g., Person, Corporate Body, Family, Group)",
    )
    merged_status = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    parent_ulan_id = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        help_text="Parent_Subject_ID for hierarchy",
    )
    parent_string = models.TextField(
        null=True,
        blank=True,
        help_text="Parent_String ancestry chain",
    )
    parent_relationship_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Hier_Rel_Type (e.g. Instance-BTI)",
    )
    parent_historic_flag = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    # Model Methods
    def __str__(self):
        return self.ulan_id

    # Model Metadata
    class Meta:
        verbose_name = "ULAN Subject"
        verbose_name_plural = "ULAN Subjects"