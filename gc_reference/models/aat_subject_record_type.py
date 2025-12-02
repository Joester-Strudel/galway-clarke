# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class AatSubjectRecordType(SimpleBaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Record_Type value (e.g., Concept)",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "AAT Subject Record Type"
        verbose_name_plural = "AAT Subject Record Types"
