# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class IsoLanguageScope(SimpleBaseModel):
    name = models.CharField(
        max_length=255,
        help_text="ISO Language Scope Name",
    )
    
    # Model Methods
    def __str__(self):
        return self.name

    # Model Metadata
    class Meta:
        verbose_name = "ISO Language Scope"
        verbose_name_plural = "ISO Language Scopes"
