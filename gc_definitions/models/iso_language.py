# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class IsoLanguage(SimpleBaseModel):
    name = models.CharField(
        max_length=255,
        help_text="Offical name of the language",
    )
    iso_set_639_1_code = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        verbose_name="ISO 639-1 Code",
        help_text="ISO 639-1 code for the language",
    )
    iso_set_639_2_code = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        verbose_name="ISO 639-2 Code",
        help_text="ISO 639-2 code for the language",
    )
    iso_set_639_3_code = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        verbose_name="ISO 639-3 Code",
        help_text="ISO 639-3 code for the language",
    )
    iso_set_639_5_code = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        verbose_name="ISO 639-5 Code",
        help_text="ISO 639-5 code for the language",
    )
    iso_language_scope = models.ForeignKey(
        "gc_definitions.IsoLanguageScope",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ISO Language Scope",
        related_name="languages",
    )
    iso_language_type = models.ForeignKey(
        "gc_definitions.IsoLanguageType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ISO Language Type",
        related_name="languages",
    )
    getty_language_code = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Getty Language Code",
        help_text="Getty language code for the language",
    )

    # Model Methods
    def __str__(self):
        return self.name

    # Model Metadata
    class Meta:
        verbose_name = "ISO Language"
        verbose_name_plural = "ISO Languages"
