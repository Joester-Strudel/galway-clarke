# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class ZipCode(SimpleBaseModel):
    """ZIP/postal code record."""

    zip_code_five_digit = models.CharField(
        max_length=5,
        null=False,
        blank=False,
        verbose_name="ZIP Code (5 Digit)",
    )
    zip_code_nine_digit = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="ZIP Code (9 Digit)",
    )
    population = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name="Population",
    )
    density = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Density",
        help_text="Population density per square mile.",
    )
    states = models.ManyToManyField(
        "gc_geography.State",
        related_name="zip_codes",
        blank=True,
        verbose_name="States",
    )
    counties = models.ManyToManyField(
        "gc_geography.County",
        related_name="zip_codes",
        blank=True,
        verbose_name="Counties",
    )
    cities = models.ManyToManyField(
        "gc_geography.City",
        related_name="zip_codes",
        blank=True,
        verbose_name="Cities",
    )

    def __str__(self):
        return self.zip_code_five_digit

    class Meta:
        verbose_name = "ZIP Code"
        verbose_name_plural = "ZIP Codes"
        ordering = ("zip_code_five_digit",)
