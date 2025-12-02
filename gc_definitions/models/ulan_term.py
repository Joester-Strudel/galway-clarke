# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanTerm(SimpleBaseModel):
    subject = models.ForeignKey(
        "gc_definitions.UlanSubject",
        on_delete=models.CASCADE,
        related_name="terms",
    )
    term_id = models.CharField(
        max_length=32,
    )
    term_text = models.CharField(
        max_length=500,
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
    is_preferred = models.BooleanField(default=False,)
    term_type = models.ForeignKey(
        "gc_definitions.UlanTermType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Term_Type",
    )
    part_of_speech = models.ForeignKey(
        "gc_definitions.UlanPartOfSpeech",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    language_code = models.ForeignKey(
        "gc_definitions.IsoLanguage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    qualifier = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.term_text

    class Meta:
        verbose_name = "ULAN Term"
        verbose_name_plural = "ULAN Terms"
