# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class County(SimpleBaseModel):
    """County within a state."""

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="County",
    )
    fips_code = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="FIPS Code",
    )
    state = models.ForeignKey(
        "gc_geography.State",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="State",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "County"
        verbose_name_plural = "Counties"
        ordering = ("state", "name")
