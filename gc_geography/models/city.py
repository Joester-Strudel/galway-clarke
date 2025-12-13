# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class City(SimpleBaseModel):
    """City within a state/county."""

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="City",
    )
    state = models.ForeignKey(
        "gc_geography.State",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="State",
    )
    county = models.ForeignKey(
        "gc_geography.County",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="County",
    )

    def __str__(self):
        state = (
            getattr(self.state, "abbreviation", None)
            or getattr(self.state, "name", None)
            or "Unknown State"
        )
        return f"{self.name} ({state})"

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        ordering = ("state", "name")
