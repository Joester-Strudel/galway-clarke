# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanPartOfSpeech(SimpleBaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Part of Speech value for ULAN terms",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ULAN Part of Speech"
        verbose_name_plural = "ULAN Parts of Speech"
