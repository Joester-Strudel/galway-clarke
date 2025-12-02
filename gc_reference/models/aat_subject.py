# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AatSubject(SimpleBaseModel):
    aat_id = models.CharField(
        max_length=32,
        unique=True,
        verbose_name="AAT Subject ID",
        help_text="Getty AAT Subject_ID",
    )
    record_type = models.ForeignKey(
        "gc_reference.AatSubjectRecordType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Record Type",
        help_text="Record_Type Field (e.g., 'Concept')",
    )
    merged_status = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Merged Status",
        help_text="Merged_Status Field",
    )
    sort_order = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Sort Order",
        help_text="Sort_Order",
    )
    parent = models.ForeignKey(
        "gc_reference.AatSubject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Parent Subject",
        help_text="Preferred parent subject",
    )
    parent_string = models.TextField(
        null=True,
        blank=True,
        verbose_name="Parent String",
        help_text="Parent_String Listing Hierarchy Ancestors",
    )
    parent_relationship_type = models.ForeignKey(
        "gc_reference.AatParentRelationshipType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Parent Relationship Type",
        help_text="Hier_Rel_Type (e.g., 'Genus/Species-BTG')",
    )

    # Model Methods
    def __str__(self):
        return self.aat_id

    def preferred_subject_name(self):
        """
        Return the first preferred term text for this subject, if any.
        """
        preferred_term = self.terms.filter(is_preferred=True).first()
        return preferred_term.term_text if preferred_term else None

    # Model Metadata
    class Meta:
        verbose_name = "AAT Subject"
        verbose_name_plural = "AAT Subjects"
