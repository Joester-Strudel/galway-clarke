# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanNationality(SimpleBaseModel):
    subject = models.ForeignKey(
        "gc_reference.UlanSubject",
        on_delete=models.CASCADE,
        related_name="nationalities",
    )
    nationality_code = models.CharField(
        max_length=100,
        help_text="e.g., 901600/French",
    )
    display_order = models.IntegerField(
        null=True,
        blank=True,
    )
    is_preferred = models.BooleanField(default=False)

    def __str__(self):
        return self.nationality_code

    class Meta:
        verbose_name = "ULAN Nationality"
        verbose_name_plural = "ULAN Nationalities"
