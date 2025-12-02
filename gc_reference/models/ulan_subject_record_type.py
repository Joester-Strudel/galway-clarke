# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanSubjectRecordType(SimpleBaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Record_Type (e.g., Person, Corporate Body, Family, Group)",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ULAN Subject Record Type"
        verbose_name_plural = "ULAN Subject Record Types"
