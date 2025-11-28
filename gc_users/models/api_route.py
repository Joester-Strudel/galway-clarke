# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models.simple_base_model import SimpleBaseModel


class ApiRoute(SimpleBaseModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Name",
        help_text="A human-readable name for this API key.",
    )

    # Model Methods
    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "API Route"
        verbose_name_plural = "API Routes"
