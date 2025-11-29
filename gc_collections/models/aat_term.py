# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AATTerm(SimpleBaseModel):
    subject = models.ForeignKey(
        "gc_collections.AATSubject",
        on_delete=models.CASCADE,
        related_name="terms",
    )
    term_id = models.CharField(
        max_length=32,
        help_text="Term_ID inside <Preferred_Term> or <Non-Preferred_Term>",
    )
    term_text = models.CharField(
        max_length=500,
        help_text="Primary term text",
    )
    display_name = models.CharField(
        max_length=500,
        null=True,
        blank=True,
    )
    historic_flag = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    vernacular = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    is_preferred = models.BooleanField(
        default=False,
    )
    term_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Descriptor, Alternate Descriptor, Used For Term, etc.",
    )
    part_of_speech = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    language_code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Parsed from language field (e.g., '70051/English')",
    )
    qualifier = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )

    # Model Methods
    def __str__(self):
        return self.term_text

    # Model Metadata
    class Meta:
        verbose_name = "AAT Term"
        verbose_name_plural = "AAT Terms"
