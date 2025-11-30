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
        help_text="ISO 639-1 code for the language",
    )
    iso_set_639_2_code = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        help_text="ISO 639-2 code for the language",
    )
    iso_set_639_3_code = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        help_text="ISO 639-3 code for the language",
    )
    iso_set_639_5_code = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        help_text="ISO 639-5 code for the language",
    )
    
    # Model Methods
    def __str__(self):
        return self.name

    # Model Metadata
    class Meta:
        verbose_name = "ISO Language"
        verbose_name_plural = "ISO Languages"
